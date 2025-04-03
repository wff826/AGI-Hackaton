from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from session import get_session
from database import get_db
from llm_model import initial_input, chatbot

router = APIRouter()

@router.get("/recommend-programs")
async def recommend_programs(
    user_session: dict = Depends(get_session)
):
    student_info = user_session["data"].get("student_info", {})
    user_input = f"{student_info.get('name', '')},\
        {student_info.get('major', '')}, \
        {student_info.get('year', '')}, \
        {student_info.get('grade', '')} 장학금 추천"
    results = initial_input(user_input)
    user_session["data"]["programs"] = results
    return {"programs": results}

@router.post("/chatbot")
async def final_result(
    additional_input: str = Body(..., embed=True, description="추가 입력"),
    user_session: dict = Depends(get_session)
):
    student_info = user_session["data"].get("student_info", {})
    recommended_programs = user_session["data"].get("programs", [])
    prompt = f"""
    사용자 정보: {student_info}
    추천 프로그램들: {recommended_programs}
    추가 사용자 질문/입력: {additional_input}
    """
    result = chatbot(prompt)
    return {"response": result}
    