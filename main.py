from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# to run server: uvicorn main:app --reload
# to show document {serverurl}/doc

students = {
    1: {
        "name": "morad",
        "age": 22,
        "year": "test"
    }
}


class Student(BaseModel):
    name: str
    age: int
    year: str
    student_id: int


@app.get("/")
def index():
    return {"name": "First Data"}


@app.get("/students")
def get_students():
    return students


@app.get("/student/{student_id}")
# that mean its need to be int
# to add query params u can add directly to the function and to make it optinal add = None or with Optional avalible from fastapi
# u can not add optional query before required one we use * at the first to aviod these errors
def get_student(*, student_id: int = Path(None, description="The ID of the student u want to get data", gt=0), name: Optional[str] = None, test: int):
    data = students[student_id]
    return data


@app.post("/student/create")
def create_student(student: Student):
    if (student.student_id in students):
        return {
            "msg": "this id already exist"
        }

    students[student.student_id] = {
        "name": student.name,
        "age": student.name,
        "year": student.year
    }

    return student.student_id
