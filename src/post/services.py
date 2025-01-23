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
        post_dict = post.__dict__
        post_dict["username"] = username
        result.append(post_dict)

    return result

# get post by post id
def get_post_from_post_id_svc(db: Session, post_id: int) -> PostSchema:
    return db.query(Post).filter(Post.id == post_id).first()

def delete_post_svc(db: Session, post_id:int):
    post = get_post_from_post_id_svc(db, post_id)
    db.delete(post)
    db.commit()
