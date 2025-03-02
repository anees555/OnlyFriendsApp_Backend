from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date


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


class DetailedSentRequest(BaseModel):
    request_id: int
    request: FriendRequest
    username: str
    profile_pic: Optional[str] = None
    interests: list[str]


class DetailedReceivedRequest(BaseModel):
    request_id: int
    request: FriendRequest
    username: str
    profile_pic: Optional[str] = None
    interests: List[str]


class DetailedFriendRequests(BaseModel):
    sent_requests: List[DetailedSentRequest]
    received_requests: List[DetailedReceivedRequest]


class Friend(BaseModel):
    user_id: int
    fullname: str
    username: str

    profile_pic: Optional[str] = None


class FriendRequestTable(BaseModel):
    request_id: int
    sender_id: int
    receiver_id: int
    status: str