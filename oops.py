# Ctrl + ? - To add comments

# OOPs - Object Oriented Programming

# Class - Blueprint
# Object - Copy of Blueprint (instance of a class)

# Indentation is very important in Python (gap) i

# Syntax:
# class className:
#       attributes (entities)
#       behaviors (methods)
import random

number = 10
name = "Akshay"

print(type(number))
print(type(name))

class Student:
    # Constructor
    # dunder method - double underscore
    # Initializing the values for attributes
    def __init__(self, name, branch):
        self.name = name
        self.branch = branch

    def welcome(self):
        print("Welcome to NIE College!")

    # def registerStudent(self, Name, Branch):
    def registerStudent(self):
        # Assigning the USN for the student
        num = random.randint(1, 100)
        # self.name = Name
        # self.branch = Branch
        print("Thank You for registering your admission in our college.")
        print("Please check your admission details:")
        print(f"Name: {self.name}")
        print(f"USN: 4NI25CS{num:03d}")
        print(f"Branch: {self.branch}")
        print(f"Semester: 1")
        print(f"Section: 'A'")

    def announcement(self, message):
        print(f"Dear Students of {self.branch}, {message}")

# Create an Object of Student Class
# object_name = class_name(paramters)

student1 = Student("Akshay", "CSE")

student1.welcome()
student1.registerStudent()
student1.announcement("Classes will start from 9:00 AM")

print(type(student1))

student2 = Student("Ajay", "ISE")

student2.welcome()
student2.registerStudent()
student2.announcement("Please assemble at Auditorium for Orientation Program")

print(type(student2))