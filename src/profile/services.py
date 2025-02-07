from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from .schemas import ProfileCreate, ProfileUpdate, Profile as ProfileSchema
from .models import Profile
from ..auth.models import User
from ..auth.schemas import User as UserSchema

import os

def save_profile_picture(file: UploadFile, user_id: int) -> str:
    # Ensure the upload directory exists

    UPLOAD_DIRECTORY = "profile_pictures"

    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

    # Define the file path
    file_extension = file.filename.split(".")[-1]
    file_name = f"user_{user_id}_profile.{file_extension}"
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)

    # Save the file locally
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path

def create_profile_svc(db: Session, profile: ProfileCreate, user_id:int, profile_pic: UploadFile = None):
    #check if a profile already exits for a user
    existing_profile = db.query(Profile).filter(Profile.user_id==user_id).first()
    if existing_profile:
        raise ValueError("User already has a profile")
    
    profile_pic_url = None
    if profile_pic:
        profile_pic_url = save_profile_picture(profile_pic, user_id)
    db_profile = Profile(
        date_of_birth=profile.date_of_birth,
        gender=profile.gender,
        location=profile.location,
        interests=profile.interests,
        profile_pic=profile_pic_url,
        user_id=user_id
    )

    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_user_profile_svc(db:Session, user_id:int) -> ProfileSchema:
    existing_profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not existing_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile does not exist for the user"
        )
    
    return existing_profile

def update_profile_svc(
    db: Session, profile_data: ProfileCreate, user_id: int, profile_pic: UploadFile = None
):
    # Fetch the existing profile
    existing_profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not existing_profile:
        raise ValueError("Profile does not exist for the user")

    # Update the profile picture if provided
    if profile_pic:
        profile_pic_url = save_profile_picture(profile_pic, user_id)
        existing_profile.profile_pic = profile_pic_url

    # Update only the fields that are provided
    if profile_data.date_of_birth:
        existing_profile.date_of_birth = profile_data.date_of_birth
    if profile_data.gender:
        existing_profile.gender = profile_data.gender
    if profile_data.location:
        existing_profile.location = profile_data.location
    if profile_data.interests:
        existing_profile.interests = profile_data.interests

    db.commit()
    db.refresh(existing_profile)
    return existing_profile



