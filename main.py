from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models, schemas, crud
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

origins = [
    "http://localhost:5173",  # React dev server
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Create DB tables
Base.metadata.create_all(bind=engine)

# ✅ Register student
@app.post("/register", response_model=schemas.StudentOut)
def register_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    existing = crud.get_student_by_email(db, student.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_student(db, student)

# ✅ Get student data by email
@app.get("/student", response_model=schemas.StudentOut)
def get_student(email: str, db: Session = Depends(get_db)):
    student = crud.get_student_by_email(db, email)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
