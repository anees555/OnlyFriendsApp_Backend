from sqlalchemy import Column, Date, DateTime, Integer, String, ForeignKey


from ..database import Base
from datetime import datetime
from sqlalchemy.orm  import relationship
from ..post.models import post_votes
from ..profile.models import user_interest_association 

class User(Base):
    __tablename__ = "users"

    # basic details
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())

    profile = relationship("Profile", back_populates="user", uselist=False)

    post = relationship("post.models.Post", back_populates="author")

    voted_posts = relationship(
        "post.models.Post", secondary=post_votes, back_populates="voted_by_users"
    )

    interests = relationship("Interest", secondary=user_interest_association, back_populates="users")
