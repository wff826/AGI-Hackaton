from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    location: str
    income: Optional[int] = None
    job: str
    enterprise_size: Optional[str] = None
    
    class Config:
        model_config = {"from_attributes": True}

class UserResponse(UserCreate):
    id: int
    class Config:
        model_config = {"from_attributes": True}