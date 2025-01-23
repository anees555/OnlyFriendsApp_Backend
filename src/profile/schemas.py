from pydantic import BaseModel
from typing import  Optional
from datetime  import datetime, date
from .enums import Gender

class ProfileBase(BaseModel):
    date_of_birth: Optional[date]
    gender: Optional[Gender]
    location: Optional[str]
    interests: Optional[str]

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass 

class Profile(ProfileBase):
    id: int
    user_id: int
    profile_pic: Optional[str]

    class Config:
        from_attributes = True
        

    