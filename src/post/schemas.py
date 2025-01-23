from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostCreate(BaseModel):
    content: Optional[str] = None

class Post(PostCreate):
    id: int
    author_username: str
    created_at: datetime

    class Config:
        from_attributes = True
