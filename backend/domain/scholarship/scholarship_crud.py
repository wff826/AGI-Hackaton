# scholarship_crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from models import Scholarship 
from .scholarship_schema import ScholarshipName, ScholarshipRawText


async def create_scholarship(db: AsyncSession, Name: ScholarshipName, RawText: ScholarshipRawText):
    """
    추출된 enrollment 정보와 grade 정보를 합쳐 Student 테이블에 저장.
    """
    db_scholarship = Scholarship(
        name=Name.name,
        raw_text=RawText.raw_text
    )
    db.add(db_scholarship)
    await db.commit()  # 비동기 방식으로 변경
    await db.refresh(db_scholarship)
    return db_scholarship

