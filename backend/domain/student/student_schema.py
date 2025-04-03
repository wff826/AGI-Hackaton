# student_schema.py
from pydantic import BaseModel

class EnrollmentInfo(BaseModel):
    """
    수강(등록) 정보를 담기 위한 스키마
    - 이름, 학번, 학과, 학년
    """
    name: str
    studentid: str
    major: str
    year: str


class GradeInfo(BaseModel):
    """
    성적 정보를 담기 위한 스키마
    - 성적(등급)
    """
    grade: str
