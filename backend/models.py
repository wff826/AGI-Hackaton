from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.types import JSON

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True)
    location = Column(String(100), index=True)
    income = Column(Integer, nullable=True, index=True)
    job = Column(String(50), index=True)
    enterprise_size = Column(String(50), nullable=True, index=True)
    
class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=True, index=True)
    studentid = Column(String(50), nullable=True, index=True)
    major = Column(String(50), nullable=True, index=True)
    year = Column(String(50), nullable=True, index=True)
    grade = Column(String(50), nullable=True, index=True)
    
class Scholarship(Base):
    __tablename__ = "scholarships"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=True, index=True)
    raw_text = Column(String, nullable=True)
    