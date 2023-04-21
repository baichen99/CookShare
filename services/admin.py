from typing import Optional
from beanie import Document, Indexed


class Admin(Document):
    username: str
    email: str
    password: str

    class Settings:
        collection = "admin"


def get_admin_by_id(id: str):
    return Admin.find_one(Admin.id == id)

def get_admin_by_email(email: str):
    return Admin.find_one(Admin.email == email)

def get_admins(skip: int = 0, limit: int = 100, sort_by: str = "email", order: str = "asc"):
    return Admin.find().skip(skip).limit(limit).sort(sort_by, order)

def create_admin(admin: Admin):
    return admin.save()

def update_admin(admin: Admin):
    return admin.save()

def delete_admin(admin: Admin):
    return admin.delete()
