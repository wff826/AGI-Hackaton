# scholarship_crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from models import Scholarship 
from .scholarship_schema import ScholarshipName, ScholarshipRawText


async def create_scholarship(db: AsyncSession, Name: ScholarshipName, RawText: ScholarshipRawText):
    db_scholarship = Scholarship(
        name=Name.name,
        raw_text=RawText.raw_text
    )
    db.add(db_scholarship)
    await db.commit() 
    await db.refresh(db_scholarship)
    return db_scholarship

