# ✅ llm_router.py

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from session import get_session
from database import get_db
from llm_model import initial_input, chatbot  # ✅ chatbot도 import

router = APIRouter()

@router.get("/recommend-programs")
async def recommend_programs(
    db: AsyncSession = Depends(get_db),
    user_session: dict = Depends(get_session)
):
    student_info = user_session["data"].get("student_info", {})
    user_input = f"{student_info.get('name', '')}, {student_info.get('major', '')}, {student_info.get('year', '')}, {student_info.get('grade', '')} 장학금 추천"
    results = initial_input(user_input)
    user_session["data"]["programs"] = results
    return {"programs": results}


# ✅ 챗봇 API 추가 (POST 방식, 사용자 메시지 받음)
@router.post("/chatbot")
async def chatbot_response(
    request: Request,
    db: AsyncSession = Depends(get_db),
    user_session: dict = Depends(get_session)
):
    body = await request.json()
    user_input = body.get("message", "")
    response = chatbot(user_input)
    return {"response": response}
