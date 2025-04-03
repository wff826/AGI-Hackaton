# student_schema.py
from pydantic import BaseModel, Json
from typing import Optional

class ScholarshipName(BaseModel):
    """
    수강(등록) 정보를 담기 위한 스키마
    - 이름, 학번, 학과, 학년
    """
    name: Optional[str] = None


class ScholarshipRawText(BaseModel):
    """
    성적 정보를 담기 위한 스키마
    - 성적(등급)
    """
    raw_text: Optional[str] = None
