from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from session import get_session
from database import get_db
from llm_model import generate_program_titles, enrich_with_links

router = APIRouter()

@router.get("/recommend-programs")
async def recommend_programs(
    db: AsyncSession = Depends(get_db),
    user_session: dict = Depends(get_session)
):
    student_info = user_session["data"].get("student_info", {})
    user_input = f"{student_info.get('name', '')},\
        {student_info.get('major', '')}, \
        {student_info.get('year', '')}, \
        {student_info.get('grade', '')} 장학금 추천"
    programs = generate_program_titles(user_input)
    results = enrich_with_links(programs)
    user_session["data"]["programs"] = results
    return {"programs": results}
    