from fastapi import Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime
from ..config import settings

from .models import User
from .schemas import UserCreate

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # hasing password
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="v1/auth/token")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm  # encoding our jwt
TOKEN_EXPIRE_MINS = settings.access_token_expire_minutes

# check for existing user
def existing_user(db: Session, username: str, email: str):
    db_user = db.query(User).filter((User.username == username)|(User.email==email)).first()
    return db_user

# create access token
def create_access_token(username: str, id: int):
    encode = {"sub": username, "id": id}
    expires = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINS)
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# get current user from token
def get_current_user(db: Session, token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id: str = payload.get("id")
        expires: datetime = payload.get("exp")
        if datetime.fromtimestamp(expires) < datetime.now():
            return None
        if username is None or id is None:
            return None
        return db.query(User).filter(User.id == id).first()
    except JWTError:
        return None

# get user from user id
def get_user_from_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# create user
def create_user(db: Session, user: UserCreate):
    db_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email.lower().strip(),
        username=user.username.lower().strip(),
        hashed_password=bcrypt_context.hash(user.password)
    )
    db.add(db_user)
    db.commit()

    return db_user

# authentication
def authenticate(db: Session, username: str, password: str):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        print("no user")
        return None
    if not bcrypt_context.verify(password, db_user.hashed_password):
        return None
    return db_user

