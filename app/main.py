from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


students = {
    1: {"name": "Jaseem", "age": 21, "course": "MCA"},
    2: {"name": "Zasim", "age": 23, "course": "BSC(IT)"},
}


class Student(BaseModel):
    name: str
    age: int
    course: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    course: Optional[str] = None


@app.get("/")
def read_root():
    return {"status": "First API Succssful"}


@app.get("/students")
def read_students():
    return {"response": students, "message": "Successfully fetched student data"}


@app.get("/students/{student_id}")
def read_student(student_id: Optional[int] = None):
    if student_id is None:
        return {"response": "please provide a student Id"}

    if student_id not in students:
        return {"Response": "This student id donesn't exits"}

    return students[student_id]


@app.get("/get_student_by_name/{student_id}")
# * means all the parameters wrtitten after this becomes the query parameters
def get_student_by_name(*, student_id: int, name: Optional[str] = None, test: int):

    if name is None:
        return students

    result = []
    for student in students.values():
        if name.lower() in student["name"].lower():
            result.append(student)

    return (
        {"Response": "Data not found. Please Enter a valid name"}
        if not result
        else result
    )


@app.post("/create_student/{student_id}")
def create_Student(student_id: int, student: Student):
    if student_id in students.keys():
        return {"Error": f"This id already exists. Please try {len(students) + 1}"}

    students[student_id] = student.model_dump()
    return {"Response": "Student Created Successfully", **student.model_dump()}


@app.put("/update_Student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students.keys():
        return {
            "Error": "This student id doesn't exists. Please create one or use the esixting one"
        }

    if student.name is not None:
        students[student_id]["name"] = student.name

    if student.age is not None:
        students[student_id]["age"] = student.age

    if student.course is not None:
        students[student_id]["course"] = student.course

    return {"Response": "Student updated successfully", **students[student_id]}


@app.delete("/delete_student/{student_id}")
def delete_student(student_id:int):
    if student_id not in students.keys():
        return {"Error":f"Student Id {student_id} doesn't esixts in the DataBase."}
    
    del students[student_id]
    return {"Reponse":f"Student with id {student_id} is removed from the DataBase successfully"}