from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String, nullable=True)
    location = Column(String, nullable=True)
    interests = Column(String, nullable=True)
    profile_pic  = Column(String, nullable=True)

    user = relationship("auth.models.User", backref="profiles")
