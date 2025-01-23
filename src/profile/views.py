from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from ..database import get_db
from .schemas import ProfileCreate, Profile as ProfileSchema
from .services import create_profile_svc, get_user_profile_svc, update_profile_svc
from ..auth.services import get_current_user, existing_user
from ..auth.schemas import User
from .enums import Gender
from  .models import  Profile
from datetime import date
from typing import Optional

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post("/", response_model=ProfileSchema, status_code=status.HTTP_201_CREATED)
def create_profile(token: str,
                    date_of_birth: date = Form(...),
                    gender: Gender = Form(...),
                    location: str = Form(...),
                    interests: str = Form(...),
                    profile_pic: UploadFile=File(None), 
                    db: Session = Depends(get_db)):
    # verify the token
    user =  get_current_user(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized."
        )
 
    profile = ProfileCreate(
        date_of_birth=date_of_birth,
        gender=gender,
        location=location,
        interests=interests,
    )

    # Check and create the profile
    try:
        db_profile = create_profile_svc(db, profile, user.id, profile_pic)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    return db_profile

@router.get("/myprofile", response_model=ProfileSchema)
def get_current_user_profile(token:str, db:Session=Depends(get_db)):
    user = get_current_user(db,  token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized."
        )
    return get_user_profile_svc(db, user.id)

@router.get("/user/{username}", response_model=ProfileSchema)
def get_user_profile(username:str, db:Session=Depends(get_db)):
    user = existing_user(db, username, "")
    return get_user_profile_svc(db, user.id)

@router.put("/", response_model=ProfileSchema, status_code=status.HTTP_200_OK)
def update_profile(
    token: str,
    date_of_birth: Optional[date] = Form(None),
    gender: Optional[Gender] = Form(None),
    location: Optional[str] = Form(None),
    interests: Optional[str] = Form(None),
    profile_pic: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    # Verify the token
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

    profile_data = ProfileCreate(
        date_of_birth=date_of_birth or existing_profile.date_of_birth,
        gender=gender or existing_profile.gender,
        location=location or existing_profile.location,
        interests=interests or existing_profile.interests
    )

    # Update the profile
    try:
        updated_profile = update_profile_svc(db, profile_data, user.id, profile_pic)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

    return updated_profile


