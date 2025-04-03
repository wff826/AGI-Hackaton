from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

# upstage_info.py 안의 추출 함수를 import
from upstage_info import call_info_extract
from upstage import call_upstage_api

# DB 세션 주입을 위한 의존성 함수를 직접 구현하거나, 프로젝트 구조에 맞게 수정
from database import get_db
from session import get_session

# CRUD 함수와 스키마 import
from .scholarship_crud import create_scholarship
from .scholarship_schema import ScholarshipName, ScholarshipRawText

router = APIRouter()
@router.post("/scholarship")
async def upload_scholarship(
    scholarship_file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user_session: dict = Depends(get_session)
):

    # 1) PDF 파일을 임시로 저장
    with open("scholarship_temp.pdf", "wb") as f:
        f.write(await scholarship_file.read())

    # 2) Upstage API 등을 통해 정보 추출
    scholarship_info_dict = call_info_extract("scholarship_temp.pdf")
    scholarship_raw_dict = call_upstage_api("scholarship_temp.pdf")

    # 3) Pydantic 스키마에 매핑 (추출된 JSON을 스키마 형태에 맞게 변환)
    scholarship_name = ScholarshipName(**scholarship_info_dict)
    scholarship_raw = ScholarshipRawText(raw_text=scholarship_raw_dict)

    # 4) DB에 저장
    scholarship = await create_scholarship(db, scholarship_name, scholarship_raw)

    user_session["data"]["scholarship_info"] = {
        "id": scholarship.id,
        "name": scholarship.name,
        "raw_text": scholarship.raw_text
    }
    return {
        "message": "Scholarship information uploaded and saved successfully.",
        "scholarship": user_session["data"]["scholarship_info"]
    }