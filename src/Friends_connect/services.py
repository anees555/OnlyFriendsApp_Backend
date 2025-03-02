from sqlalchemy.orm import Session
from ..auth.models import User
from .models import FriendRequest
from .schemas import (
    FriendRequestCreate,
    FriendRequestUpdate,
    DetailedSentRequest,
    DetailedReceivedRequest,
    DetailedFriendRequests,
)
from ..similarity.models import Similarity
from ..profile.models import Interest
from ..auth.models import user_interest_association


def accept_update_similarity_status(db: Session, user_id: int, similar_user_id: int):
    suggestions = (
        db.query(Similarity)
        .filter(
            (Similarity.user_id == user_id) | (Similarity.similar_user_id == user_id)
        )
        .all()
    )
    for suggestion in suggestions:
        if (
            suggestion.user_id == similar_user_id
            or suggestion.similar_user_id == similar_user_id
        ):
            suggestion.is_active = False
            db.commit()


def reject_update_similarity_status(db: Session, user_id: int, similar_user_id: int):
    suggestions = (
        db.query(Similarity)
        .filter(
            (Similarity.user_id == user_id) | (Similarity.similar_user_id == user_id)
        )
        .all()
    )
    for suggestion in suggestions:
        if (
            suggestion.user_id == similar_user_id
            or suggestion.similar_user_id == similar_user_id
        ):
            suggestion.is_active = True
            db.commit()


def send_friend_request(db: Session, sender_id: int, receiver_id: int):
    receiver = db.query(User).filter(User.id == receiver_id).first()
    if not receiver:
        return False, "Receiver not found"
    existing_request = (
        db.query(FriendRequest)
        .filter(
            FriendRequest.sender_id == sender_id,
            FriendRequest.receiver_id == receiver_id,
        )
        .first()
    )
    if existing_request:
        return False, "Friend request already sent"

    friend_request = FriendRequest(
        sender_id=sender_id, receiver_id=receiver_id, status="pending"
    )
    db.add(friend_request)
    db.commit()
    db.refresh(friend_request)

    accept_update_similarity_status(db, sender_id, receiver_id)

    return True, friend_request


def accept_friend_requests(db: Session, request_id: int):
    friend_request = (
        db.query(FriendRequest).filter(FriendRequest.id == request_id).first()
    )
    if not friend_request:
        return False, "Request not found"

    friend_request.status = "accepted"
    db.commit()
    db.refresh(friend_request)

    # Remove from suggestion list without deleting from the database
    accept_update_similarity_status(
        db, friend_request.sender_id, friend_request.receiver_id
    )

    return True, friend_request


def reject_friend_requests(db: Session, request_id: int):
    friend_request = (
        db.query(FriendRequest).filter(FriendRequest.id == request_id).first()
    )
    if not friend_request:
        return False, "Request not found"

    db.delete(friend_request)


    # Remove from suggestion list without deleting from the database
    # update_similarity_status(db, friend_request.sender_id, friend_request.receiver_id)

    reject_update_similarity_status(
        db, friend_request.sender_id, friend_request.receiver_id
    )
    
    return True, friend_request


def get_friend_requests(db: Session, user_id: int) -> DetailedFriendRequests:
    sent_requests = (
        db.query(FriendRequest)
        .filter(FriendRequest.sender_id == user_id, FriendRequest.status == "pending")
        .all()
    )
    received_requests = (
        db.query(FriendRequest)
        .filter(FriendRequest.receiver_id == user_id, FriendRequest.status == "pending")
        .all()
    )

    detailed_sent_requests = []
    for request in sent_requests:
        receiver = db.query(User).filter(User.id == request.receiver_id).first()
        interests = (
            db.query(Interest)
            .join(user_interest_association)
            .filter(user_interest_association.c.user_id == receiver.id)
            .all()
        )
        interest_names = [interest.name for interest in interests]

        detailed_sent_requests.append(
            DetailedSentRequest(
                request_id=request.id,
                request=request,
                username=receiver.username,
                profile_pic=receiver.profile.profile_pic if receiver.profile else None,
                interests=interest_names,
            )
        )

    detailed_received_requests = []
    for request in received_requests:
        sender = db.query(User).filter(User.id == request.sender_id).first()
        interests = (
            db.query(Interest)
            .join(user_interest_association)
            .filter(user_interest_association.c.user_id == sender.id)
            .all()
        )
        interest_names = [interest.name for interest in interests]

        detailed_received_requests.append(
            DetailedReceivedRequest(
                request_id=request.id,
                request=request,
                username=sender.username,
                profile_pic=sender.profile.profile_pic if sender.profile else None,
                interests=interest_names,
            )
        )

    return DetailedFriendRequests(
        sent_requests=detailed_sent_requests,
        received_requests=detailed_received_requests,
    )


def get_friends(db: Session, user_id: int):
    accepted_requests = (
        db.query(FriendRequest)
        .filter(
            (
                (FriendRequest.sender_id == user_id)
                | (FriendRequest.receiver_id == user_id)
            )
            & (FriendRequest.status == "accepted")
        )
        .all()
    )

    friends = []

    for request in accepted_requests:
        if request.sender_id == user_id:
            friend = db.query(User).filter(User.id == request.receiver_id).first()
        else:
            friend = db.query(User).filter(User.id == request.sender_id).first()

        friends.append(
            {
                "user_id": friend.id,
                "fullname": f"{friend.firstname} {friend.lastname}",
                "username": friend.username,
                "profile_pic": friend.profile.profile_pic if friend.profile else None,
            }
        )

    return friends


def get_request_table(
    db: Session,
):
    pass

def unsend_friend_request(db: Session, sender_id: int, receiver_id: int):
    friend_request = db.query(FriendRequest).filter(
        FriendRequest.sender_id == sender_id,
        FriendRequest.receiver_id == receiver_id,
        FriendRequest.status == "pending"
    ).first()

    if not friend_request:
        return False, f"You have not sent the friend to user_id {receiver_id}"
    
    reject_update_similarity_status(db, friend_request.sender_id, friend_request.receiver_id)


    db.delete(friend_request)
    db.commit()

    return True, "Friend request unsent successfully"



