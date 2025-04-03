# scholarship_crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from models import Student
from .student_schema import StudentEnrollment, StudentGrade


async def create_student(db: AsyncSession, Enrollment: StudentEnrollment, Grade: StudentGrade):
    """
    추출된 enrollment 정보와 grade 정보를 합쳐 Student 테이블에 저장.
    """
    db_student = Student(
        name=Enrollment.name,
        studentid=Enrollment.studentid,
        major=Enrollment.major,
        year=Enrollment.year,
        grade=Grade.grade
    )
    db.add(db_student)
    await db.commit()  # 비동기 방식으로 변경
    await db.refresh(db_student)
    return db_student

