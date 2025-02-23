from sqlalchemy.orm import Session
from ..auth.models import User
from .models import FriendRequest
from .schemas import FriendRequestCreate
# from fastapi import HTTPException, status

def send_friend_request(db: Session, sender_id: int, receiver_id: int):
    receiver = db.query(User).filter(User.id == receiver_id).first()
    if not receiver:
        return False, "Receiver not found"
    existing_request = db.query(FriendRequest).filter(
        FriendRequest.sender_id == sender_id,
        FriendRequest.receiver_id == receiver_id
    ).first()
    if existing_request:
        return False, "Friend request already sent"

    friend_request = FriendRequest(
        sender_id=sender_id,
        receiver_id=receiver_id,
        status="pending"
    )
    db.add(friend_request)
    db.commit()
    db.refresh(friend_request)
    return True, friend_request

def accept_friend_requests(db: Session, request_id: int):
    friend_requests = db.query(FriendRequest).filter(FriendRequest.id == request_id).first()
    if not friend_requests:
        return False, "Request not found"
    
    friend_requests.status = "accepted"
    db.commit()
    db.refresh(friend_requests)
    return True, friend_requests
         
def reject_friend_requests(db: Session, request_id: int):
    friend_request = db.query(FriendRequest).filter(FriendRequest.id == request_id).first()
    if not friend_request:
        return False, "Request not found"
    friend_request.status = "rejected"
    db.commit()
    db.refresh(friend_request)
    return friend_request

def get_friend_requests(db: Session, user_id: int):
    sent_requests = db.query(FriendRequest).filter(FriendRequest.sender_id == user_id).all()
    received_requests = db.query(FriendRequest).filter(FriendRequest.receiver_id == user_id).all()
    return sent_requests, received_requests

def get_friends(db: Session, user_id: int):
    accepted_requests = db.query(FriendRequest).filter((FriendRequest.sender_id == user_id) | (FriendRequest.receiver_id == user_id)) & (FriendRequest.status == "accepted").all()
    friends = []
    for request in accepted_requests:
        if request.sender_id == user_id:
            friend = db.query(User).filter(User.id == request.receiver_id).first()
        else:
            friend = db.query(User).filter(User.id == request.sender_id).first()
        friends.append(friend)
    return friends



    
    