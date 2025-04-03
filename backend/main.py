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

# ✅ 1. 주민등록등본 API
@app.post("/upload/resident")
async def upload_resident(file: UploadFile = File(...)):
    file_path = "temp_resident.pdf"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    raw_text = call_upstage_api(file_path)
    instruction = "이름, 생년, 주소를 JSON 형식으로 추출해주세요."
    extracted_info = call_info_extract(raw_text, instruction)

    return {
        "raw_text": raw_text,
        "extracted_info": extracted_info
    }


# ✅ 3. 일반 문서 API
@app.post("/upload/general")
async def upload_general(
    resident: UploadFile = File(...),
    income: UploadFile = File(...)
):
    with open("resident_temp.pdf", "wb") as f:
        f.write(await resident.read())
    with open("income_temp.pdf", "wb") as f:
        f.write(await income.read())

    resident_text = call_upstage_api("resident_temp.pdf")
    income_text = call_upstage_api("income_temp.pdf")

    combined_text = resident_text + "\n" + income_text
    instruction = "이름, 생년, 주소, 소득금액을 JSON 형식으로 추출해주세요."
    extracted_info = call_info_extract(combined_text, instruction)

    return {
        "raw_text": combined_text,
        "extracted_info": extracted_info
    }

# ✅ 라우터 등록
app.include_router(user_router, prefix="/api")
app.include_router(recommend_router)  # RAG 추천 API 라우터 연결
app.include_router(student_router, prefix="/upload")
app.include_router(scholarship_router, prefix="/upload")