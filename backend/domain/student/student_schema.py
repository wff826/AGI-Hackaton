# student_schema.py
from pydantic import BaseModel
from typing import Optional

class StudentEnrollment(BaseModel):
    """
    수강(등록) 정보를 담기 위한 스키마
    - 이름, 학번, 학과, 학년
    """
    name: Optional[str] = None
    studentid: Optional[str] = None
    major: Optional[str] = None
    year: Optional[str] = None
    


class StudentGrade(BaseModel):
    """
    성적 정보를 담기 위한 스키마
    - 성적(등급)
    """
    grade: Optional[str] = None
