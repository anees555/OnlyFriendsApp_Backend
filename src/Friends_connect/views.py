from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session 
from fastapi.security import OAuth2PasswordBearer
from ..database import get_db
from .services import send_friend_request, accept_friend_requests, reject_friend_requests, get_friend_requests, get_friends
from ..auth.services import get_current_user
from ..auth.models import User as UserSchema
from .schemas import FriendRequestCreate, FriendRequestUpdate, FriendRequest as FriendRequestSchema
from typing import List

router = APIRouter(prefix = "/friends", tags = ["Friends"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "v1/auth/token")

@router.post("/send", response_model = FriendRequestSchema)
def send_request(
    request: FriendRequestCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "You are not authorized"
        )
    success, result = send_friend_request(db, user.id, request.receiver_id)
    if not success:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = result
        )
    return result

@router.put("/accept/{request_id}", response_model = FriendRequestSchema)
def accept_request(
    request_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "You are not authrized"
        )
    success, result = accept_friend_requests(db, request_id)
    if not success:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = result
        )
    return result

@router.get("/requests", response_model = List[FriendRequestSchema])
def get_requests(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
    ):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "You are not authorized"
        )
    sent_requests, received_requests = get_friend_requests(db, user.id)
    return sent_requests + received_requests 

@router.get("/friends", response_model = None)
def get_user_friends(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )
    
    
    friends = get_friends(db, user.id)
    return friends