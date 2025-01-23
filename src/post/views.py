from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .schemas import PostCreate, Post
from .services import create_post_svc, get_user_posts_svc,get_random_posts_svc, get_post_from_post_id_svc, delete_post_svc

from ..auth.services import get_current_user, existing_user
from ..auth.schemas import User

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, token: str, db: Session = Depends(get_db)):
    # verify the token
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized."
        )

    # create post
    db_post = create_post_svc(db, post, user.username)

    return db_post

@router.get("/user", response_model=list[Post])
def get_current_user_posts(token: str, db: Session = Depends(get_db)):
    # verify the token
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized."
        )

    return get_user_posts_svc(db, user.username)

@router.get("/user/{username}", response_model=list[Post])
async def get_user_posts(username: str, db: Session = Depends(get_db)):
    # verify token
    user = existing_user(db, username, "")

    return get_user_posts_svc(db, user.username)

@router.get("/feed")
def get_random_posts(token:str,
    page: int = 1, limit: int = 5, db: Session = Depends(get_db)
):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized."
        )
    return get_random_posts_svc(db, page, limit)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(token: str, post_id: int, db: Session = Depends(get_db)):
    # verify the token
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you are not authorized to delete this post.",
        )

    post = get_post_from_post_id_svc(db, post_id)
    if post.author_username != user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you are not authorized to delete this post.",
        )

    delete_post_svc(db, post_id)
