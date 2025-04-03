from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from upstage import call_upstage_api
from upstage_info import call_info_extract
from domain.user.user_router import router as user_router
from recommend import router as recommend_router  # ✅ RAG 추천 API 추가
from domain.student.student_router import router as student_router
from domain.scholarship.scholarship_router import router as scholarship_router

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ 라우터 등록
app.include_router(user_router, prefix="/api")
app.include_router(recommend_router)  # RAG 추천 API 라우터 연결
app.include_router(student_router, prefix="/upload")
app.include_router(scholarship_router, prefix="/upload")