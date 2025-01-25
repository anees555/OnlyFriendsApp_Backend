from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base

post_votes = Table(
    "post_votes",
    Base.metadata,
    Column("user_username", String, ForeignKey("users.username")),
    Column("post_id", Integer, ForeignKey("posts.id")),
)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())
    votes_count = Column(Integer, default=0)

    author_username = Column(String, ForeignKey("users.username"))
    author = relationship("auth.models.User", back_populates="post")

    voted_by_users = relationship(
        "auth.models.User", secondary=post_votes, back_populates="voted_posts"
    )
