from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base

user_interest_association = Table(
    "user_interest_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("interest_id", Integer, ForeignKey("interests.id"))
)

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String, nullable=True)
    location = Column(String, nullable=True)
    # interests = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    profile_pic  = Column(String, nullable=True)

    user = relationship("User", back_populates = "profile")
    

    # interests =  relationship("Interest", secondary=user_interest_association, back_populates = "profiles")
    # interests = relationship("Interest", secondary=profile_interest_association, back_populates = "profiles")
  
class Interest(Base):
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    # profiles = relationship("Profile", secondary=user_interest_association, back_populates = "interests")
    # profiles = relationship("profile.models.profile", secondary=user_interest_association, back_populates = "interests")
    users = relationship("User", secondary = "user_interest_association", back_populates = "interests")