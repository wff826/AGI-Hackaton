from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True)
    location = Column(String(100), index=True)
    income = Column(Integer, nullable=True, index=True)
    job = Column(String(50), index=True)
    enterprise_size = Column(String(50), nullable=True, index=True)