from fastapi import APIRouter, Header

from api.v1.services.anti_cheat_services import insert_answers, get_exam_report

router = APIRouter()


@router.post("/insert")
async def insert_student_answers(
    submissions: dict, x_user_id: int = Header(...), x_exam_id: str = Header(...)
):
    """Insert student answers into collections"""
    return await insert_answers(submissions, x_user_id, x_exam_id)


@router.get("/report/{exam_id}")
async def exam_report(exam_id: str):
    """Detect all suspected cheaters for an exam"""
    return await get_exam_report(exam_id)
