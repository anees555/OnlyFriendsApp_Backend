from pydantic import BaseModel 
from typing import List, Optional
from datetime import datetime,  date

class FriendRequestBase(BaseModel):
    sender_id: int
    receiver_id: int
    status: Optional[str] = "pending"

class FriendRequestCreate(FriendRequestBase):
    pass

class FriendRequestUpdate(BaseModel):
    status: str

class FriendRequest(FriendRequestBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True