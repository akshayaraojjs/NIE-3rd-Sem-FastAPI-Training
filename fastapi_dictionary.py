# FastAPI is a Python Framework
# ASGI - Async Server Gateway Interface

# To handle ASGI, we use Uvicorn to act as a Server

# HTTP Status Code
# 200 - OK (Get Request)
# 201 - CREATED (POST Request)
# 204 - NO CONTENT (DELETE Request)
# 404 - NOT FOUND (When data is missing)
# 500 - Internal Server Error (Code or Server Error)

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
# students - dictionary
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
# Request - Get Method with students in the url
# Response - List of all students
@app.get("/students", response_model=list[Student])
def getAllStudents():
    # students.values() is a dictionary method
    return list(students.values())

# {student_id} - path parameter
# Request - GET Method students with "id" => students/1
# Response - Single Student data
@app.get("/students/{student_id}", response_model=Student)
def getStudent(student_id: int):
    # To check the existence of student data w.r.t dictionary
    if student_id not in students:
        raise HTTPException(
            status_code = 404,
            detail = "Student not found"
        )
    # If the student_id is available, show their info
    return students[student_id]

# Request - POST Method with students url,
# Response - Student data will be shown for the confirmation after insertion
@app.post("/students", response_model=Student, status_code=201)
# student is an object of StudentCreate class
def createStudent(student: StudentCreate):
    # max(student.keys()) will fetch the latest/biggest value from key and adds 1 to it, so next number will be incremented
    new_id = max(students.keys(), default = 0) + 1
    new_student = {
        "id": new_id,
        # ** - Unpacking of dictionary
        **student.model_dump()
    }
    # students[3] = object
    students[new_id] = new_student

    # Show the Response wiith given details 
    return new_student

# {student_id} - path parameter
# Request - PUT Method students with "id" => students/1
# Response - Single Student data
@app.put("/students/{student_id}", response_model=Student)
def updateStudent(student_id: int, student: StudentUpdate):
    # To check the existence of student data w.r.t dictionary before updating
    if student_id not in students:
        raise HTTPException(
            status_code = 404,
            detail = "Student not found"
        )

    # Update to the existing data similar to insertion
    students[student_id] = {
        "id" : student_id,
        **student.model_dump()
    }

    # Show the Response wiith updated details 
    return students[student_id]

# {student_id} - path parameter
# Request - DELETE Method students with "id" => students/1
# Response - Show only message
@app.delete("/students/{student_id}")
def deleteStudent(student_id: int):
    # To check the existence of student data w.r.t dictionary before deleting
    if student_id not in students:
        raise HTTPException(
            status_code = 404,
            detail = "Student not found"
        )

    # Deleting the students data using del keyword
    del students[student_id]

    return {
        "message" : "Student details deleted successfully"
    }

# uvicorn fastapi_dictionary:app --reload 

# Client (Browser)
#         ↓  HTTP Request
# Uvicorn           ← ASGI Server (runs the app)
#         ↓  ASGI
# FastAPI           ← Your API code
#         ↓
# Pydantic          ← Validates request data
#         ↓
# Business Logic
#         ↓  HTTP Response (JSON)
# Client