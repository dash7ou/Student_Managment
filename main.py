from fastapi import FastAPI, Path, Response, status
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


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


@app.get("/", status_code=200)
def index():
    return {"name": "First Data"}


@app.get("/students", status_code=200)
def get_students():
    return students


@app.get("/student/{student_id}", status_code=200)
# that mean its need to be int
# to add query params u can add directly to the function and to make it optinal add = None or with Optional avalible from fastapi
# u can not add optional query before required one we use * at the first to aviod these errors
def get_student(*, student_id: int = Path(None, description="The ID of the student u want to get data", gt=0), name: Optional[str] = None, test: int, response: Response):
    if (student_id not in students):
        response.status_code = 404
        return {
            "msg": "User Not Found!"
        }

    data = students[student_id]
    return data


@app.post("/student/create", status_code=201)
def create_student(student: Student, response: Response):
    if (student.student_id in students):
        response.status_code = 400
        return {
            "msg": "this id already exist"
        }

    students[student.student_id] = {
        "name": student.name,
        "age": student.name,
        "year": student.year
    }

    response.status_code = 201
    return student.student_id


@app.put("/student/{student_id}", status_code=200)
def update_student(student_id: int, student: UpdateStudent, response: Response):
    if student_id not in students:
        response.status_code = 404
        return {
            "msg": "Student does not exist!"
        }

    if student.name:
        students[student_id]["name"] = student.name

    if student.age:
        students[student_id]["age"] = student.age

    if student.year:
        students[student_id]["year"] = student.year

    return student_id


@app.delete("/student/{student_id}", status_code=200)
def delete_student(student_id: int, response: Response):
    if student_id not in students:
        response.status_code = 404
        return {
            "msg": "Student does not exist!"
        }

    del students[student_id]
    return {
        "msg": "success"
    }
