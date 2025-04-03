from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from upstage import call_upstage_api
from upstage_info import call_info_extract
from domain.user.user_router import router as user_router

app = FastAPI()

# CORS 설정 (프론트 연결 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중이니 전체 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 1. 주민등록등본 업로드 API (기존)
@app.post("/upload/resident")
async def upload_resident(file: UploadFile = File(...)):
    file_path = "temp.pdf"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 1. 문서에서 텍스트 추출
    raw_text = call_upstage_api(file_path)

    # 2. InfoExtract로 구조화 정보 추출
    instruction = "이름, 생년, 주소를 JSON 형식으로 추출해주세요."
    extracted_info = call_info_extract(raw_text, instruction)

    return {
        "raw_text": raw_text,
        "extracted_info": extracted_info
    }

# ✅ 2. 학생용 문서 업로드 API (추가)
@app.post("/upload/student")
async def upload_student(
    enrollment: UploadFile = File(...),
    grade: UploadFile = File(...)
):
    # 파일 저장
    with open("enrollment.pdf", "wb") as f:
        f.write(await enrollment.read())
    with open("grade.pdf", "wb") as f:
        f.write(await grade.read())

    # TODO: 여기에 Upstage API 호출 및 정보 추출 붙이면 됨
    return {
        "message": "Student documents uploaded successfully!",
        "files": [enrollment.filename, grade.filename]
    }

# ✅ 라우터 등록
app.include_router(user_router, prefix="/api")
