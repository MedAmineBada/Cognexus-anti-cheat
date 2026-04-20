from datetime import datetime

from qdrant_client.models import PointStruct

from api.v1.utils.helpers import lowercase_submissions, clean_text
from config import (
    ensure_collection,
    get_qdrant_client,
    SIMILARITY_THRESHOLD,
    model_instance,
)


async def insert_answers(submissions: dict, student: int, exam: str):
    """Insert student answers into Qdrant collections"""
    lowercase = lowercase_submissions(submissions)
    cleaned = {}

    for exercise_number, questions in lowercase.items():
        for question_id, answer_text in questions.items():
            cleaned[question_id] = clean_text(answer_text)

    vdb = get_qdrant_client()
    results = {}

    for question_id, answer_text in cleaned.items():
        embedding = model_instance.model.encode(answer_text)
        collection_name = ensure_collection(exam, question_id)

        # Upsert embedding only
        try:
            vdb.upsert(
                collection_name=collection_name,
                points=[
                    PointStruct(
                        id=student,
                        vector=embedding.tolist(),
                        payload={
                            "student_id": student,
                            "exam_id": exam,
                            "question_id": question_id,
                            "timestamp": datetime.now().isoformat(),
                        },
                    )
                ],
            )
            results[question_id] = {"status": "inserted"}
        except Exception as e:
            print(f"Insert error for {collection_name}: {e}")
            results[question_id] = {"status": "failed", "error": str(e)}

    return results


async def detect_all_cheaters(exam: str):
    """Detect all suspected cheaters for an exam by comparing all answers"""
    vdb = get_qdrant_client()

    # Get all collections for this exam
    all_collections = vdb.get_collections().collections
    exam_collections = [
        c.name for c in all_collections if c.name.startswith(f"{exam}_Q")
    ]

    cheat_report = {}

    for collection_name in exam_collections:
        question_id = collection_name.split("_Q")[-1]  # Extract question ID

        try:
            # Get all points in collection
            all_points_response = vdb.scroll(
                collection_name=collection_name,
                limit=10000,
                with_vectors=True,  # ← Include vector data
            )
            all_points = all_points_response[0]  # First element is the points list

            question_cheaters = []

            # Compare each student against all others
            for i, point in enumerate(all_points):
                student_id = point.id
                embedding = point.vector

                # Search for similar answers
                search_results = vdb.query_points(
                    collection_name=collection_name,
                    query=embedding,
                    limit=len(all_points),  # Search all
                    score_threshold=SIMILARITY_THRESHOLD,
                ).points

                # Filter out self and build matches
                matches = []
                for result in search_results:
                    if result.id != student_id:  # Exclude self
                        matches.append(
                            {
                                "student_id": result.id,
                                "similarity": round(result.score, 4),
                            }
                        )

                # If suspicious matches found
                if matches:
                    question_cheaters.append(
                        {
                            "student_id": student_id,
                            "suspicious": True,
                            "max_similarity": round(
                                max([m["similarity"] for m in matches]), 4
                            ),
                            "matches": matches,
                        }
                    )

            cheat_report[question_id] = question_cheaters

        except Exception as e:
            print(f"Detection error for {collection_name}: {e}")
            cheat_report[question_id] = {"error": str(e)}

    return cheat_report
