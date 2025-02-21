from fastapi import APIRouter, Depends, status, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime
from .schemas import UserCreate, User as UserSchema
from ..database import get_db
from  .services import (
    existing_user,
    create_access_token,
    get_current_user,
    create_user as  create_user_svc,
    authenticate
)

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token")

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # check existing user
    db_user = existing_user(db, user.username, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username or email already in use",
        )

    db_user = create_user_svc(db, user)
    access_token = create_access_token(user.username, db_user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
    }

# login to generate token
@router.post("/token", status_code=status.HTTP_201_CREATED)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = authenticate(db, form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
        )

    access_token = create_access_token(db_user.username, db_user.id)
    return {"access_token": access_token, "token_type": "bearer"}

# get current user
@router.get("/current_user", status_code=status.HTTP_200_OK, response_model=UserSchema)
def current_user(token: str = Header(...), db: Session = Depends(get_db)):
    db_user = get_current_user(db, token)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid"
        )

    return db_user

@router.get("/user_info", status_code=status.HTTP_200_OK)
def get_user_info(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    db_user = get_current_user(db, token)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized."
        )

    return {
        "username": db_user.username,
        "full_name": f"{db_user.firstname} {db_user.lastname}"
    }