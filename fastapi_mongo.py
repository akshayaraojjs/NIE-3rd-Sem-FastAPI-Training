# Authentication - Signup/Register & Login/Signin

# Authorization - Check for Permissions based on the User Role before accessing

# API Endpoint - Method + URL

# Payload - Data sent in a Body while requesting
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
# pymongo is used to establish connection b/w Python/FastAPI with MongoDB
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional
# To store the password in Hash using "Argon2"
from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone


# =========================================================
# 1. FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Student Management API",
    description="FastAPI + MongoDB + JWT Authentication + RBAC",
    version="4.0.0"
)


# =========================================================
# 2. MONGODB
# =========================================================

MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

db = client["mongo_student_management"]

students_collection = db["students"]
users_collection = db["users"]


# =========================================================
# 3. ROLE CONSTANTS
# =========================================================
# 1 = Admin
# 2 = Teacher
# 3 = Student

ADMIN_ROLE = 1
TEACHER_ROLE = 2
STUDENT_ROLE = 3


# =========================================================
# 4. PASSWORD HASHING
# =========================================================

password_hash = PasswordHash.recommended()


# =========================================================
# 5. JWT CONFIGURATION
# =========================================================

SECRET_KEY = "StudentAppSecurityKey"  # Change this in production

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# =========================================================
# 6. OAUTH2
# =========================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


# =========================================================
# 7. PYDANTIC MODELS
# =========================================================

# While using POST request (/students - endpoint) with Payload, this BaseModel is used for validation
class StudentCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=50
    )

    age: int = Field(
        ge=5,
        le=100
    )

    course: str = Field(
        min_length=2,
        max_length=50
    )

    # Required when Admin wants to link a student
    # record with a Student-role user.
    user_id: Optional[str] = None


class StudentUpdate(BaseModel):

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50
    )

    age: Optional[int] = Field(
        default=None,
        ge=5,
        le=100
    )

    course: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50
    )


class StudentResponse(BaseModel):

    id: str
    name: str
    age: int
    course: str
    user_id: Optional[str] = None


class UserCreate(BaseModel):

    # Field method from pydantic is used for validation 
    username: str = Field(
        min_length=3,
        max_length=30
    )

    password: str = Field(
        min_length=6
    )

    role: int = Field(
        ge=1,
        le=3
    )


class TokenResponse(BaseModel):

    access_token: str
    token_type: str


# =========================================================
# 8. HELPER FUNCTIONS
# =========================================================


# If POST/GET Request is success for /students, then the response is sent in this format
def student_helper(student) -> dict:

    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "age": student["age"],
        "course": student["course"],
        "user_id": (
            str(student["user_id"])
            if student.get("user_id")
            else None
        )
    }


def user_helper(user) -> dict:

    # when user is created with a request, this is the response format shown to the client 
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "role": user["role"]
    }


# =========================================================
# 9. CREATE JWT
# =========================================================


def create_access_token(username: str, role: int):

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "role": role,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# =========================================================
# 10. GET CURRENT USER
# =========================================================


def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")
        role = payload.get("role")

        if username is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    # If token has expired after 30 mins, this error will be shown
    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = users_collection.find_one(
        {"username": username}
    )

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


# =========================================================
# 11. ROLE AUTHORIZATION
# =========================================================


def require_roles(*allowed_roles):

    def role_checker(
        current_user=Depends(get_current_user)
    ):

        if current_user["role"] not in allowed_roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        return current_user

    return role_checker


# =========================================================
# 12. STUDENT OWNERSHIP HELPER
# =========================================================


def get_my_student(current_user):

    """
    Returns the student record linked to the logged-in user.

    Student records must contain:
        user_id: ObjectId(<user's MongoDB _id>)
    """

    student = students_collection.find_one(
        {
            "user_id": current_user["_id"]
        }
    )

    if student is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found for this user"
        )

    return student


# =========================================================
# 13. HOME
# =========================================================


@app.get("/")
def home():

    return {
        "message": "Student Management API",
        "version": "4.0.0"
    }


# =========================================================
# 14. CREATE USER
# =========================================================
#
# For workshop/demo setup only.
#
# Role:
# 1 = Admin
# 2 = Teacher
# 3 = Student
#
# In a production application, this endpoint should
# itself be protected according to the required policy.
# =========================================================


@app.post("/users")
def create_user(user: UserCreate):

    # db.users.findOne({"username" : "aarav_admin"})
    existing_user = users_collection.find_one(
        {"username": user.username}
    )

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    hashed_password = password_hash.hash(
        user.password
    )

    # User Request
    user_data = {
        "username": user.username,
        "password": hashed_password,
        "role": user.role
    }

    # ORM - insertOne ()=> insert_one()
    result = users_collection.insert_one(
        user_data
    )

    # Once the user is created the primary key (_id) is assigned automatically by MongoDB
    created_user = users_collection.find_one(
        {"_id": result.inserted_id}
    )

    return user_helper(created_user)


# =========================================================
# 15. LOGIN
# =========================================================


@app.post(
    "/login",
    response_model=TokenResponse
)
    # expecting username & password in the login request in the form
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = users_collection.find_one(
        {"username": form_data.username}
    )

    if user is None:

        # If user is not found raise exception with status code 401 - UNAUTHORIZED and message
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not password_hash.verify(
        form_data.password,
        user["password"]
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token(
        user["username"],
        user["role"]
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================================================
# 16. GET ALL STUDENTS
# =========================================================
#
# ADMIN   -> Allowed
# TEACHER -> Allowed
# STUDENT -> NOT ALLOWED
#
# Student can use GET /students/me to view only
# their own student record.
# =========================================================


@app.get(
    "/students",
    response_model=list[StudentResponse]
)
# Admin & Teacher has the permission to access
def get_students(
    current_user=Depends(
        require_roles(
            ADMIN_ROLE,
            TEACHER_ROLE
        )
    )
):

    students = students_collection.find()

    return [
        student_helper(student)
        for student in students
    ]


# =========================================================
# 17. GET CURRENT STUDENT PROFILE
# =========================================================
#
# ADMIN   -> Not required for this endpoint
# TEACHER -> Not required for this endpoint
# STUDENT -> Gets ONLY their own student data
#
# This endpoint is provided specifically for Student role.
# =========================================================


@app.get(
    "/students/me",
    response_model=StudentResponse
)
def get_my_student_profile(
    current_user=Depends(
        require_roles(STUDENT_ROLE)
    )
):

    student = get_my_student(current_user)

    return student_helper(student)


# =========================================================
# 18. GET ONE STUDENT
# =========================================================
#
# ADMIN   -> Can view any student
# TEACHER -> Can view any student
# STUDENT -> Can view ONLY their own student
# =========================================================


@app.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: str,
    current_user=Depends(get_current_user)
):

    if not ObjectId.is_valid(student_id):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student ID"
        )

    student = students_collection.find_one(
        {"_id": ObjectId(student_id)}
    )

    if student is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # Student can access ONLY their own record.
    if current_user["role"] == STUDENT_ROLE:

        # If they try to access other's ID, access will be denied
        if student.get("user_id") != current_user["_id"]:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Students can only view their own data"
            )

    # Teacher and Admin can view any student.

    # No one can access other than 3 rolese: 1, 2 & 3
    if current_user["role"] not in (
        ADMIN_ROLE,
        TEACHER_ROLE,
        STUDENT_ROLE
    ):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

    return student_helper(student)


# =========================================================
# 19. CREATE STUDENT
# =========================================================
#
# ADMIN   -> Allowed
# TEACHER -> NOT ALLOWED
# STUDENT -> NOT ALLOWED
#
# Admin can optionally provide user_id to link a
# Student-role login account with the student record.
# =========================================================

# 
@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
# Before creating the student, first check for Admin role
def create_student(
    student: StudentCreate,
    current_user=Depends(
        require_roles(ADMIN_ROLE)
    )
):

    # Request should be sent in this format for Payload
    student_data = {
        "name": student.name,
        "age": student.age,
        "course": student.course
    }

    # -----------------------------------------------------
    # If user_id is provided, validate and link it.
    # -----------------------------------------------------

    if student.user_id:

        # Check the user_id before accepting
        if not ObjectId.is_valid(student.user_id):

            # If unknown user_id is sent in request, throw 400 - BAD Request
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID"
            )

        linked_user = users_collection.find_one(
            {"_id": ObjectId(student.user_id)}
        )

        if linked_user is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if linked_user["role"] != STUDENT_ROLE:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only a Student-role user can be linked to a student profile"
            )

        existing_student = students_collection.find_one(
            {"user_id": ObjectId(student.user_id)}
        )

        if existing_student:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This user already has a student profile"
            )

        student_data["user_id"] = ObjectId(student.user_id)

    result = students_collection.insert_one(
        student_data
    )

    created_student = students_collection.find_one(
        {"_id": result.inserted_id}
    )

    return student_helper(created_student)


# =========================================================
# 20. UPDATE STUDENT
# =========================================================
#
# ADMIN   -> Can update any student
# TEACHER -> Can update any student
# STUDENT -> Can update ONLY their own student record
# =========================================================


@app.put(
    "/students/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: str,
    student: StudentUpdate,
    current_user=Depends(get_current_user)
):

    if not ObjectId.is_valid(student_id):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student ID"
        )

    student_object_id = ObjectId(student_id)

    existing_student = students_collection.find_one(
        {"_id": student_object_id}
    )

    if existing_student is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # -----------------------------------------------------
    # Student can update ONLY their own profile.
    # -----------------------------------------------------

    if current_user["role"] == STUDENT_ROLE:

        if existing_student.get("user_id") != current_user["_id"]:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Students can only update their own data"
            )

    # -----------------------------------------------------
    # Only Admin, Teacher and the owning Student can reach
    # this point.
    # -----------------------------------------------------

    if current_user["role"] not in (
        ADMIN_ROLE,
        TEACHER_ROLE,
        STUDENT_ROLE
    ):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )

    update_data = student.model_dump(
        exclude_unset=True
    )

    if not update_data:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )

    result = students_collection.update_one(
        {"_id": student_object_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    updated_student = students_collection.find_one(
        {"_id": student_object_id}
    )

    return student_helper(updated_student)


# =========================================================
# 21. DELETE STUDENT
# =========================================================
#
# ADMIN   -> Allowed
# TEACHER -> NOT ALLOWED
# STUDENT -> NOT ALLOWED
# =========================================================


@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_student(
    student_id: str,
    current_user=Depends(
        require_roles(ADMIN_ROLE)
    )
):

    if not ObjectId.is_valid(student_id):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student ID"
        )

    result = students_collection.delete_one(
        {"_id": ObjectId(student_id)}
    )

    if result.deleted_count == 0:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return None

# | Operation               | Admin | Teacher |    Student |
# | ----------------------- | ----: | ------: | ---------: |
# | View all students       |     ✅ |   ✅ |          ❌ |
# | View individual student |     ✅ |   ✅ | ✅ Own only |
# | View own profile        |     ✅ |   ✅ |          ✅ |
# | Create student          |     ✅ |   ❌ |          ❌ |
# | Update student          |     ✅ |   ✅ | ✅ Own only |
# | Delete student          |     ✅ |   ❌ |          ❌ |
