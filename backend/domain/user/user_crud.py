from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from domain.user.user_schema import UserCreate

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user