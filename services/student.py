from typing import Optional, List
from beanie import Document
from beanie import PydanticObjectId
from beanie.exceptions import DocumentNotFound
from beanie.operators import Eq, RegEx
from pydantic import EmailStr
from models.student import StudentQuery


class Student(Document):
    username: str
    email: EmailStr
    password: str

    class Settings:
        collection = "student"
        
    def to_dict(self):
        d = {}
        for k, v in self.dict().items():
            # convert ObjectId to str
            if k == 'id':
                d['id'] = str(v)
            else:
                d[k] = v
        return d


async def get_student_by_id(id: PydanticObjectId):
    student = await Student.get(id)
    return student

async def get_student_by_email(email: str):
    student = await Student.find_one(Student.email == email)
    return student

async def get_students(query: StudentQuery) -> List[Student]:
    query_list = []
    if query.username:
        query_list.append(RegEx(Student.username, query.username))
    if query.email:
        query_list.append(Eq(Student.email, query.email))
    students = await Student.find_many(
        *query_list
    ).skip(query.skip).limit(query.limit).sort(
        (query.sort_by, query.order)
        ).to_list()
    return students

async def create_student(student: Student) -> Student:
    student_ = await student.create()
    return student_

async def update_student(id: PydanticObjectId, student: Student) -> Student:
    student_ = await get_student_by_id(id)
    if not student_:
        raise DocumentNotFound
    values = student.dict(exclude_unset=True)
    for key, value in values.items():
        setattr(student_, key, value)
    await student_.save()
    return student_

async def delete_student(id: PydanticObjectId) -> bool:
    student = await Student.find_one(Student.id == id)
    if student:
        await student.delete()
        return True
