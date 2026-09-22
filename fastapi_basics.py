# API - Application Programming Interface

# It acts like a bridge

# Client Requests

# Server Respond

# from fastapi library import the FastAPI module
from fastapi import FastAPI

# initialize the fast api application in variable app 
app = FastAPI()

# FastAPI server runs in this url:
# http://127.0.0.1:8000

# http://localhost:8000/

# http: HyperText Transfer Protocol

# 127.0.0.1 - localhost (To run the server in our local system)

# 8000 - port number

# 5 Methods used for Request & Response
# 1) GET - To Read or Fetch some data (Read)
# 2) POST - To insert the data (Create)
# 3) PUT - To update the existing data (Update)
# 4) DELETE - To delete the data (Delete)
# 5) PATCH - To update some/partial part of the data (Update)

# API endpoint
# Base Route
@app.get("/")
def home():
    return {
        "message": "This is a Home URL"
    }

@app.get("/students")
def getAllStudents():
    return {
        "message": "Fetching all students data"
    }

@app.get("/students/{student_id}")
def getStudentDetails(student_id: int):
    return {
        "message": f"Fetching details of Student {student_id}"
    }

@app.post("/students")
def createStudent():
    return {
        "message": "Student details created successfully"
    }

@app.put("/students/{student_id}")
def updateStudentDetails(student_id: int):
    return {
        "message": f"Updating the details of Student {student_id}"
    }

@app.delete("/students/{student_id}")
def deleteStudentDetails(student_id: int):
    return {
        "message": f"Deleting the details of Student {student_id}"
    }
# uvicorn file_name:app

# uvicorn fastapi_basics:app

# uvicorn fastapi_basics:app --reload

# To use Swagger UI for testing the API:
# 127.0.0.1:8000/docs