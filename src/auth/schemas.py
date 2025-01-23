from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    username: str
    firstname: str
    lastname: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime