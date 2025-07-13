from sqlalchemy.orm import Session
from models import Student
from schemas import StudentCreate

def create_student(db: Session, student: StudentCreate):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_student_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email).first()
