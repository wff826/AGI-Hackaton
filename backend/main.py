from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from domain.user.user_router import router as user_router
from recommend import router as recommend_router  # ✅ RAG 추천 API 추가
from domain.scholarship.scholarship_router import router as scholarship_router
from session import create_session, get_session

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/create-session")
async def session_endpoint():
    session_id = create_session()
    return {"session_token": session_id}


# ✅ 라우터 등록
app.include_router(user_router, prefix="/api")
app.include_router(recommend_router)  # RAG 추천 API 라우터 연결
app.include_router(scholarship_router, prefix="/upload")