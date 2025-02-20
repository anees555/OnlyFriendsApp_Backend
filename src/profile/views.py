from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Form, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from ..database import get_db
from .schemas import ProfileCreate, ProfileUpdate, Profile as ProfileSchema
from .services import create_profile_svc, get_user_profile_svc, update_profile_svc, add_interest_to_user, get_user_interests, update_user_interests
from ..auth.services import get_current_user, existing_user
from ..auth.schemas import User
from .enums import Gender
from .models import Profile, Interest

router = APIRouter(prefix="/profile", tags=["Profile"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token")

@router.get("/interests", response_model=List[str])
def get_all_interests(db: Session = Depends(get_db)):
    interests = db.query(Interest).all()
    return [interest.name for interest in interests]

@router.post("/add-interests", response_model=List[str], status_code=status.HTTP_201_CREATED)
def add_interests(
    token: str = Depends(oauth2_scheme),
    interests: List[str] = Form(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized."
        )

    return add_interest_to_user(db, user.id, interests)

@router.put("/update-interests", response_model=List[str], status_code=status.HTTP_200_OK)
def update_interests(
    token: str = Depends(oauth2_scheme),
    interests: List[str] = Form(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized."
        )

    return update_user_interests(db, user.id, interests)

@router.post("/", response_model=ProfileSchema, status_code=status.HTTP_201_CREATED)
def create_profile(
    token: str = Depends(oauth2_scheme),
    date_of_birth: date = Form(...),
    gender: Gender = Form(...),
    location: str = Form(...),
    bio: Optional[str] = Form(None),
    profile_pic: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized."
        )
    
    interests = get_user_interests(db, user.id)
    if not interests:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You must add interests before creating a profile."
        )

    profile = ProfileCreate(
        date_of_birth=date_of_birth,
        gender=gender,
        location=location,
        bio=bio,
        interests=interests
    )

    try:
        db_profile = create_profile_svc(db, profile, user.id, profile_pic)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    
    return db_profile

@router.put("/", response_model=ProfileSchema, status_code=status.HTTP_200_OK)
def update_profile(
    token: str = Depends(oauth2_scheme),
    date_of_birth: Optional[date] = Form(None),
    gender: Optional[Gender] = Form(None),
    location: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    profile_pic: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized."
        )
    existing_profile = db.query(Profile).filter(Profile.user_id == user.id).first()
    if not existing_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found."
        )

    profile_data = ProfileUpdate(
        date_of_birth=date_of_birth or existing_profile.date_of_birth,
        gender=gender or existing_profile.gender,
        location=location or existing_profile.location,
        bio=bio or existing_profile.bio,
    )

    try:
        updated_profile = update_profile_svc(db, profile_data, user.id, profile_pic)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    return updated_profile

@router.get("/myprofile", response_model=ProfileSchema)
def get_current_user_profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized."
        )
    return get_user_profile_svc(db, user.id)

@router.get("/user/{username}", response_model=ProfileSchema)
def get_user_profile(username: str, db: Session = Depends(get_db)):
    user = existing_user(db, username, "")
    profile = get_user_profile_svc(db, user.id)
    return profile

@router.get("/myprofile/interests", response_model=List[str])
def get_current_user_interests(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized."
        )
    return get_user_interests(db, user.id)



