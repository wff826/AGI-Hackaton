from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ 라우터 임포트
from domain.student.student_router import router as student_router
from domain.scholarship.scholarship_router import router as scholarship_router
from recommend_router import router as recommend_router  # 또는 llm_router
from session import create_session

app = FastAPI()

# ✅ Swagger 설정
app.swagger_ui_init_oauth = {
    "usePkceWithAuthorizationCodeGrant": True
}

# ✅ CORS 설정
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
app.include_router(student_router, prefix="/upload")
app.include_router(scholarship_router, prefix="/upload")
app.include_router(recommend_router, prefix="/recommend")  # or llm_router
