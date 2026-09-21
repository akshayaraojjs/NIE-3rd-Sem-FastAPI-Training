# Python is a Programming Language. USed in various fields like Scripting, Web Development, Machine Learning, AI 

# This is a comment in Python
# variables
name = "Akshay"
age = 25
company = "MTD" 
height = 5.2
isTrainer = True
technologies = ["Python", "MongoDB", "REST API", "FastAPI", "React"]
frontend_skills = ("HTML", "CSS", "JS", "BS")
trainings = {
    "college" : "NIE",
    "branch" : "CSE",
    "sem" : 3,
    "type" : "SDP",
    "duration": 6
 }

# Ctrl + Shift + ~ - Open Terminal

# Shift + Alt + Bottom Arrow - Clone Line

# Ctrl + D - Multi-cursor
print(name, type(name)) #str - string
print(age, type(age)) # int - integer
print(company, type(company)) # str- string
print(height, type(height)) # float - decimal value
print(technologies, type(technologies)) #list - store multiple data together
print(frontend_skills, type(frontend_skills)) # tuple - store more data but not changeable
print(isTrainer, type(isTrainer)) # boolean - True or False
print(trainings, type(trainings)) # dictionary - key-value pairs

# Functions or Methods

# What is function?
# Function is a set of instructions used to perform repeatitive tasks when it is called.

# Parts of Function
# 1) Function Declaration
# 2) Function Definition
# 3) Function Call

# Syntax:
# def function_name():
#       instructions

# Function Declaration
def sayHello():
# Function Definition
    print("Hello, Welcome to NIE College!")

# Function Call
sayHello()
sayHello()
sayHello()
sayHello()

# function with parameters
# the variable within the paranthesis in function definition is called as "parameter"
# Ex: sayHi(name), name is a parameter

# the variable within the paranthesis in function call is called as "argument"
# Ex: sayHi("Akshay"), "Akshay" is an argument
def sayHi(name):
    print(f"Hi {name}, Welcome to FastAPI Training!")

sayHi("Akshay")
sayHi("Ajay")
sayHi("Aruna")
sayHi("Amulya")
sayHi("Arvind")