from pydantic import BaseModel, Field, ValidationError

class Student(BaseModel):
    name: str = Field(..., min_length=1, description="姓名")
    age: int = Field(..., ge=0, le=120, description="年龄")
    gpa: float = Field(..., ge=0.0, le=4.0, description="绩点")
    
try:
    s = Student(name="Alice", age=20, gpa=3.5)
    print(s)
except ValidationError as e:
    print(e)
    
try:
    s = Student(name="", age=150, gpa=5.0)  # Invalid data
except ValidationError as e:
    print(e.json())