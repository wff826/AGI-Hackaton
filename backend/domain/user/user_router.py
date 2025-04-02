from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from domain.user.user_schema import UserCreate, UserResponse
from domain.user.user_crud import create_user

router = APIRouter()

@router.post("/users/", response_model=UserResponse)
async def create_user_api(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db=db, user=user)