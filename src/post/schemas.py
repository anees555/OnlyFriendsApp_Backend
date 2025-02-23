from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    author_username: str
    created_at: datetime

    class Config:
        orm_mode = True
