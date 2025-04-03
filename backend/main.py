# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 라우터 import
from domain.student.student_router import router as student_router
from domain.scholarship.scholarship_router import router as scholarship_router
from session import create_session
from llm_router import router as llm_router

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 프론트 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/create-session")
async def session_endpoint():
    session_id = create_session()
    return {"session_token": session_id}

# 라우터 등록
app.include_router(student_router, prefix="/upload")
app.include_router(scholarship_router, prefix="/upload")
app.include_router(llm_router)
