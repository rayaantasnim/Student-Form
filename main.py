from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
students = [
    {"id": 1, "name": "Gennady Korotkevich", "age": 32},
    {"id": 2, "name": "Benjamin Qi", "age": 25},
    {"id": 3, "name": "Jiang Lingyu", "age": 23},
    {"id": 4, "name": "Petr Mitrichev", "age": 41},
    {"id": 5, "name": "Makoto Soejima", "age": 34},
    {"id": 6, "name": "Neal Wu", "age": 34},
    {"id": 7, "name": "Scott Wu", "age": 29},

    {"id": 8, "name": "Magnus Carlsen", "age": 35},
    {"id": 9, "name": "Garry Kasparov", "age": 63},
    {"id": 10, "name": "Viswanathan Anand", "age": 56},
    {"id": 11, "name": "Vladimir Kramnik", "age": 51},
    {"id": 12, "name": "Ding Liren", "age": 34},
    {"id": 13, "name": "Dommaraju Gukesh", "age": 20}
]


class Student(BaseModel):
    name: str
    age: int

# Home page
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"students": students}
    )

# READ
@app.get("/students")
def get_students():
    return students

# CREATE
@app.post("/students")
def create_student(student: Student):
    new_student = {
        "id": len(students) + 1,
        "name": student.name,
        "age": student.age
    }
    students.append(new_student)
    return new_student


# UPDATE
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    for s in students:
        if s["id"] == student_id:
            s["name"] = student.name
            s["age"] = student.age
            return s

    return {"message": "Student not found"}


# DELETE
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for s in students:
        if s["id"] == student_id:
            students.remove(s)
            for new_id, student in enumerate(students, start=1):
                student["id"] = new_id
            return {"message": "Student deleted"}

    return {"message": "Student not found"}
