from fastapi import APIRouter, Depends, status, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.sql import desc
from typing import List

from ..database import get_db
from .schemas import PostCreate, Post
from .services import (
    create_post_svc,
    get_user_posts_svc,
    get_random_posts_svc,
    get_post_from_post_id_svc,
    delete_post_svc,
    vote_post_svc,
    unvote_post_svc,
    voted_users_post_svc,
    get_voted_posts_svc,
    search_posts_svc,
)

from ..auth.services import get_current_user, existing_user
from ..auth.schemas import User

router = APIRouter(prefix="/posts", tags=["posts"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token")

@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    # Verify the token
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized."
        )
   
    # Create post
    db_post = create_post_svc(db, post, user.username)

    return db_post

@router.get("/user", response_model=List[Post])
def get_current_user_posts(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Verify the token
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized."
        )

    return get_user_posts_svc(db, user.username)

@router.get("/user/{username}", response_model=List[Post])
async def get_user_posts(username: str, db: Session = Depends(get_db)):
    # Verify token
    user = existing_user(db, username, "")

    return get_user_posts_svc(db, user.username)

@router.get("/feed")
def get_random_posts(
    token: str = Depends(oauth2_scheme),
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized."
        )
    return get_random_posts_svc(db, page, limit)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, token: str = Depends(oauth2_scheme),  db: Session = Depends(get_db)):
    # Verify the token
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to delete this post.",
        )

    post = get_post_from_post_id_svc(db, post_id)
    if post.author_username != user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to delete this post.",
        )

    delete_post_svc(db, post_id)
@router.post("/vote", status_code=status.HTTP_200_OK)
def vote_or_unvote_post(post_id: int, action: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Verify the token
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized."
        )

    if action == "vote":
        res, detail = vote_post_svc(db, post_id, user.username)
        if res:
            return {"detail": "voted"}
    elif action == "unvote":
        res, detail = unvote_post_svc(db, post_id, user.username)
        if res:
            return {"detail": "unvoted"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid action")

    if not res:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
    
@router.get("/votes/{post_id}", response_model=List[User])
def users_like_post(post_id: int, db: Session = Depends(get_db)):
    return voted_users_post_svc(db, post_id)

@router.get("/voted", response_model=List[Post])
def get_voted_posts(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    # Verify the token
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized."
        )

    # Get voted posts
    return get_voted_posts_svc(db, user.username)

@router.get("/search", response_model=List[Post])
def search_posts(
    query: str,
    token: str = Depends(oauth2_scheme),
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Search posts by content using a query string.
    """
    # Verify the token
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized."
        )

    # Search posts
    return search_posts_svc(db, query, page, limit)

@router.get("/{post_id}", response_model=Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    db_post = get_post_from_post_id_svc(db, post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid post ID"
        )

    return db_post