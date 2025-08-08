# understanding Pydantic
import pydantic
from datetime import date
from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel, Field, field_validator
import json

class Department(Enum):
    HR = "HR"
    SALES = "SALES"
    IT = "IT"
    ENGINEERING = "ENGINEERING"

# class Employee(BaseModel):
#     employee_id: UUID = uuid4()
#     name: str
#     date_of_birth: date
#     salary: float
#     department: Department
#     elected_benefits: bool

# # crearting a class object
# X = Employee(
#     name="Chris DeTuma",
#     date_of_birth="1998-04-02",
#      salary=123_000.00,
#      department="IT",
#      elected_benefits=True)
# print(X)

# # # providing a wrong value
# # X1 = Employee(
# #     name="Chris DeTuma",
# #     date_of_birth="1998-04-02",
# #      salary=123_000.00,
# #      department=3,
# #      elected_benefits=True)
# # # validating the value
# # print(X)

# # validating a dict and JSON before creating object
# X1_dict = {
#     "name": "ADSDSF",
#     "date_of_birth": "1998-04-02",
#     "salary": 123000.00,
#     "department": "IT",
#     "elected_benefits": True}
# # validating the value
# X1 = Employee.model_validate(X1_dict)
# # dumping into JSON or dicu
# print(X1.model_dump())
# print(X1.model_dump_json())

# # get the schema
# print(json.dumps(Employee.model_json_schema()))

# # using Pydantic Field
# class Employee1(BaseModel):
#     employee_id: UUID = Field(default_factory=uuid4, frozen=True)
#     name: str = Field(min_length=1, frozen=True)
#     date_of_birth: date = Field(alias="birth_date", repr=False, frozen=True)
#     salary: float = Field(alias="compensation", gt=0, repr=False)
#     department: Department
#     elected_benefits: bool
# '''
# - frozen: This is a Boolean parameter you can set to make your fields immutable. 
# This means, when frozen is set to True, the corresponding field can’t be changed after your model is instantiated. 
# - repr: This Boolean parameter determines whether a field is displayed in the model’s field representation. 
# In this example, you won’t see date_of_birth or salary when you print an Employee instance.
# - alias: You can use this parameter when you want to assign an alias to your fields. For example, you can allow date_of_birth 
# to be called birth_date or salary to be called compensation. You can use these aliases when instantiating or serializing a model.
# '''

# # crearting a class object
# Y = Employee1(
#     name="Chris DeTuma",
#     birth_date="1998-04-02",
#     compensation=10.0,
#     department="IT",
#     elected_benefits=True)
# print(Y)

# # chnage the repr values
# Y.department = "HR"
# print(Y)
# Y.name= "Rohan"         # cannot change
# print(Y)

# using field_validator for validation
# using Pydantic Field
class Employee2(BaseModel):
    employee_id: UUID = Field(default_factory=uuid4, frozen=True)
    name: str = Field(min_length=1, frozen=True)
    date_of_birth: date = Field(alias="birth_date", repr=False, frozen=True)
    salary: float = Field(alias="compensation", gt=0, repr=False)
    department: Department
    elected_benefits: bool

    @field_validator("date_of_birth")
    @classmethod
    def check_valid_age(cls, date_of_birth: date) -> date:
        today = date.today()
        eighteen_years_ago = date(today.year - 18, today.month, today.day)

        if date_of_birth > eighteen_years_ago:
            raise ValueError("Employees must be at least 18 years old.")

        return date_of_birth
    

# crearting a class object
Z = Employee2(
    name="Chris DeTuma",
    birth_date="2018-04-02",   # date validation fails
    compensation=10.0,
    department="IT",
    elected_benefits=True)
print(Z)