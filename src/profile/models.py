from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime

from ..database import Base

profile_interest_association = Table(
    "profile_interest_association",
    Base.metadata,
    Column("profile_id", Integer, ForeignKey("profiles.id")),
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

    user = relationship("User", backref = "profiles")
    

    interests =  relationship("Interest", secondary=profile_interest_association, back_populates = "profiles")
    # interests = relationship("Interest", secondary=profile_interest_association, back_populates = "profiles")
  
class Interest(Base):
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    profiles = relationship("Profile", secondary=profile_interest_association, back_populates = "interests")
    # profiles = relationship("profile.models.profile", secondary=profile_interest_association, back_populates = "interests")