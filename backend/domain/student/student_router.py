from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

# upstage_info.py 안의 추출 함수를 import
from upstage_info import call_info_extract

# DB 세션 주입을 위한 의존성 함수를 직접 구현하거나, 프로젝트 구조에 맞게 수정
from database import get_db
from session import get_session

# CRUD 함수와 스키마 import
from .student_crud import create_student
from .student_schema import StudentEnrollment, StudentGrade

router = APIRouter()
@router.post("/student")
async def upload_scholarship(
    enrollment_file: UploadFile = File(...),
    grade_file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user_session: dict = Depends(get_session)
):

    # 1) PDF 파일을 임시로 저장
    with open("enrollment_temp.pdf", "wb") as f:
        f.write(await enrollment_file.read())
    with open("grade_temp.pdf", "wb") as f:
        f.write(await grade_file.read())
        
    # 2) Upstage API 등을 통해 정보 추출
    enrollment_info_dict = call_info_extract("enrollment_temp.pdf")
    grade_info_dict = call_info_extract("grade_temp.pdf")

    # 3) Pydantic 스키마에 매핑 (추출된 JSON을 스키마 형태에 맞게 변환)
    enrollment_info = StudentEnrollment(**enrollment_info_dict)
    grade_info = StudentGrade(**grade_info_dict)

    # 4) DB에 저장
    student = await create_student(db, enrollment_info, grade_info)

    user_session["data"]["student_info"] = {
        "id": student.id,
        "name": student.name,
        "studentid": student.studentid,
        "major": student.major,
        "year": student.year,
        "grade": student.grade
    }
    return {
        "message": "Scholarship information uploaded and saved successfully.",
        "student": user_session["data"]["student_info"]
    }