from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from .enums import Gender

class ProfileBase(BaseModel):
    date_of_birth: Optional[date]
    gender: Optional[Gender]
    location: Optional[str]
    bio: Optional[str]
    # interests: Optional[List[str]]

class ProfileCreate(ProfileBase):
    interests: List[str]

class ProfileUpdate(ProfileBase):
    interests: Optional[List[str]]

class Profile(ProfileBase):
    id: int
    user_id: int
    profile_pic: Optional[str]
    interests: Optional[List[str]]

    class Config:
        from_attributes = True
        


