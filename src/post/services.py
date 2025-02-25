from sqlalchemy.orm import Session
import re
from sqlalchemy import desc

from .schemas import PostCreate, Post as PostSchema
from .models import Post
from ..auth.models import User
from ..auth.schemas import User as UserSchema

def create_post_svc(db:Session, post:PostCreate, user_username:str):
    db_post = Post(
        content=post.content,
        author_username=user_username
    )
    db.add(db_post)
    db.commit()
    
    return db_post

def get_user_posts_svc(db:Session, user_username:str):
    posts = (
        db.query(Post)
        .filter(Post.author_username == user_username)
        .order_by(desc(Post.created_at))
        .all()
    )
    return posts

# return latest posts of all users
def get_random_posts_svc(
    db: Session, page: int = 1, limit: int =  10
):
    total_posts = db.query(Post).count()

    offset = (page - 1) * limit
    if offset >= total_posts:
        return []

    posts = db.query(Post, User.username).join(User).order_by(desc(Post.created_at))
 


    posts = posts.offset(offset).limit(limit).all()

    result = []
    for post, username in posts:
        post_dict = post.__dict__.copy()
        if "username" in post_dict:
            del post_dict["username"]
        # post_dict["username"] = username
        result.append(post_dict)

    return result

# get post by post id
def get_post_from_post_id_svc(db: Session, post_id: int) -> PostSchema:
    return db.query(Post).filter(Post.id == post_id).first()

def delete_post_svc(db: Session, post_id:int):
    post = get_post_from_post_id_svc(db, post_id)
    db.delete(post)
    db.commit()

#vote post
def vote_post_svc(db: Session, post_id: int, username: str):
    post = get_post_from_post_id_svc(db, post_id)
    if not post:
        return False, "invalid post_id"

    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False, "invalid username"

    if user in post.voted_by_users:
        return False, "already voted"

    # increase like count of post
    post.voted_by_users.append(user)
    post.votes_count = len(post.voted_by_users)

    db.commit()
    db.refresh(post)

    return True, "done"

# unlike post
def unvote_post_svc(db: Session, post_id: int, username: str):
    post = get_post_from_post_id_svc(db, post_id)
    if not post:
        return False, "invalid post_id"

    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False, "invalid username"

    if not user in post.voted_by_users:
        return False, "already not voted"

    post.voted_by_users.remove(user)
    post.votes_count = len(post.voted_by_users)

    db.commit()
    db.refresh(post)
    return True, "done"

# users who liked post
def voted_users_post_svc(db: Session, post_id: int) -> list[UserSchema]:
    post = get_post_from_post_id_svc(db, post_id)
    if not post:
        return []
    voted_users = post.voted_by_users
    # return [UserSchema.from_orm(user) for user in liked_users]
    return voted_users

def get_voted_posts_svc(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        print(f"user not found: {username}")
        return []
    
    voted_posts = user.voted_posts 
    print(f"Voted posts for user {username}: {[post.id for post in voted_posts]}")

    result = [
        {
            "id": post.id,
            "content": post.content,
            "votes_count": post.votes_count,
            "created_at": post.created_at,
            "author_username": post.author_username,
        }
        for post in voted_posts
    ]

    return result

def search_posts_svc(db: Session, query: str, page: int = 1, limit: int = 10):
    """
    Search posts by content using a case-insensitive match.
    """
    offset = (page - 1) * limit

    # Perform case-insensitive search using `ilike`
    posts = (
        db.query(Post)
        .filter(Post.content.ilike(f"%{query}%"))
        .order_by(desc(Post.created_at))
        .offset(offset)
        .limit(limit)
        .all()
    )

    result = [
        {
            "id": post.id,
            "content": post.content,
            "votes_count": post.votes_count,
            "created_at": post.created_at,
            "author_username": post.author_username,
        }
        for post in posts
    ]

    return result









