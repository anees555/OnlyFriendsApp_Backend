from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())

    author_username = Column(String, ForeignKey("users.username"))
    author = relationship("auth.models.User", back_populates="post")