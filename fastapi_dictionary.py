# HTTPException is used to handle the errors
from fastapi import FastAPI, HTTPException
# pydantic is used for Handling Request Format & Validation
from pydantic import BaseModel

# Initializing the app to work as FastAPI application
app = FastAPI()

# Blueprint to get the data in the specified way while using POST Request
class StudentCreate(BaseModel):
    name : str
    age : int
    branch : str
    course : str

# Student Class inherits the properties of StudentCreate class with "id"
class Student(StudentCreate):
    id : int

# Blueprint to get the data in the specified fromat while using PUT Request
class StudentUpdate(BaseModel):
    name : str
    age : int
    branch : str
    course : str

# Nested Dictionary
# key is number (1, 2, 3)
# value has student details
students = {
    1 : {
        "id" : 1,
        "name" : "Akshay Rao",
        "age" : 25,
        "branch" : "CSE",
        "course" : "Python Full Stack"
    },
    2 : {
        "id" : 2,
        "name" : "Ajay Rao",
        "age" : 24,
        "branch" : "ISE",
        "course" : "Java Full Stack"
    }
}

# Base URL for Welcome Message
@app.get("/")
def home():
    return {
        "message" : "Welcome to Student Management API"
    }

# API Endpoint: Method + URL
@app.get("/students", response_model=list[Student])
def getAllStudents():
    return list(students.values())

# {student_id} - path parameter
@app.get("/students/{student_id}", response_model=Student)
def getStudent(student_id: int):
    if student_id not in students:
        raise HTTPException(
            status_code = 404,
            details = "Student not found"
        )

    return students[student_id]

@app.post("/students", response_model=Student, status_code=201)
def createStudent(student: StudentCreate):
    new_id = max(students.keys(), default = 0) + 1
    new_student = {
        "id": new_id,
        **student.model_dump()
    }
    students[new_id] = new_student

    return new_student

@app.put("/students/{student_id}", response_model=Student)
def updateStudent(student_id: int, student: StudentUpdate):
    if student_id not in students:
        raise HTTPException(
            status_code = 404,
            detail = "Student not found"
        )

    students[student_id] = {
        "id" : student_id,
        **student.model_dump()
    }

    return students[student_id]

@app.delete("/students/{student_id}")
def deleteStudent(student_id: int):
    if student_id not in students:
        raise HTTPException(
            status_code = 404,
            detail = "Student not found"
        )

    del students[student_id]

    return {
        "message" : "Student details deleted successfully"
    }

# uvicorn fastapi_dictionary:app --reload 