# student_crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from models import Student 
from .student_schema import EnrollmentInfo, GradeInfo


async def create_student(db: AsyncSession, enrollment: EnrollmentInfo, grade: GradeInfo):
    """
    추출된 enrollment 정보와 grade 정보를 합쳐 Student 테이블에 저장.
    """
    db_student = Student(
        name=enrollment.name,
        studentid=enrollment.studentid,  # models.py와 일치시킴
        major=enrollment.major,
        year=enrollment.year,
        grade=grade.grade
    )
    db.add(db_student)
    await db.commit()  # 비동기 방식으로 변경
    await db.refresh(db_student)
    return db_student

