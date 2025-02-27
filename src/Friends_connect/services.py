from sqlalchemy.orm import Session
from ..auth.models import User
from .models import FriendRequest
from .schemas import FriendRequestCreate, FriendRequestUpdate, DetailedSentRequest, DetailedReceivedRequest, DetailedFriendRequests
from ..similarity.models import Similarity

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

    # Remove from suggestion list without deleting from the database
    suggestion = db.query(Similarity).filter(
        Similarity.user_id == sender_id,
        Similarity.similar_user_id == receiver_id
    ).first()
    if suggestion:
        suggestion.is_active = False  # Assuming there's an 'is_active' field to mark it as inactive
        db.commit()

    return True, friend_request

def accept_friend_requests(db: Session, request_id: int):
    friend_request = db.query(FriendRequest).filter(FriendRequest.id == request_id).first()
    if not friend_request:
        return False, "Request not found"
    
    friend_request.status = "accepted"
    db.commit()
    db.refresh(friend_request)

    # Remove from suggestion list without deleting from the database
    suggestion = db.query(Similarity).filter(
        Similarity.user_id == friend_request.sender_id,
        Similarity.similar_user_id == friend_request.receiver_id
    ).first()
    if suggestion:
        suggestion.is_active = False
        db.commit()
    
    return True, friend_request
         
def reject_friend_requests(db: Session, request_id: int):
    friend_request = db.query(FriendRequest).filter(FriendRequest.id == request_id).first()
    if not friend_request:
        return False, "Request not found"
    
    friend_request.status = "rejected"
    db.commit()
    db.refresh(friend_request)
    
    # Remove from suggestion list without deleting from the database
    suggestion = db.query(Similarity).filter(
        Similarity.user_id == friend_request.sender_id,
        Similarity.similar_user_id == friend_request.receiver_id
    ).first()
    if suggestion:
        suggestion.is_active = False
        db.commit()
    
    return True, friend_request

def get_friend_requests(db: Session, user_id: int) -> DetailedFriendRequests:
    sent_requests = db.query(FriendRequest).filter(FriendRequest.sender_id == user_id).all()
    received_requests = db.query(FriendRequest).filter(FriendRequest.receiver_id == user_id).all()
    
    detailed_sent_requests = []
    for request in sent_requests:
        receiver = db.query(User).filter(User.id == request.receiver_id).first()
        detailed_sent_requests.append(DetailedSentRequest(
            request_id=request.id,
            request=request,
            receiver_username=receiver.username,
            receiver_profile_pic=receiver.profile.profile_pic if receiver.profile else None
        ))
    
    detailed_received_requests = []
    for request in received_requests:
        sender = db.query(User).filter(User.id == request.sender_id).first()
        detailed_received_requests.append(DetailedReceivedRequest(
            request_id=request.id,
            request=request,
            sender_username=sender.username,
            sender_profile_pic=sender.profile.profile_pic if sender.profile else None
        ))
    
    return DetailedFriendRequests(
        sent_requests=detailed_sent_requests,
        received_requests=detailed_received_requests
    )

def get_friends(db: Session, user_id: int):
    accepted_requests = db.query(FriendRequest).filter(
        ((FriendRequest.sender_id == user_id) | (FriendRequest.receiver_id == user_id)) &
        (FriendRequest.status == "accepted")
    ).all()
    
    friends = []

    for request in accepted_requests:
        if request.sender_id == user_id:
            friend = db.query(User).filter(User.id == request.receiver_id).first()
        else:
            friend = db.query(User).filter(User.id == request.sender_id).first()
        
        friends.append({
            "user_id": friend.id,
            "fullname": f"{friend.firstname} {friend.lastname}",
            "username": friend.username,
            "profile_pic": friend.profile.profile_pic if friend.profile else None
        })
    
    return friends





