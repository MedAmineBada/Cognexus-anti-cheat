from fastapi import APIRouter, Header

from api.v1.services.anti_cheat_services import insert_answers, detect_all_cheaters

router = APIRouter()


@router.post("/insert")
async def insert_student_answers(
    submissions: dict, x_student_id: int = Header(...), x_exam_id: str = Header(...)
):
    """Insert student answers into collections"""
    return await insert_answers(submissions, x_student_id, x_exam_id)


@router.get("/detect/{exam_id}")
async def detect_cheaters(exam_id: str):
    """Detect all suspected cheaters for an exam"""
    return await detect_all_cheaters(exam_id)
