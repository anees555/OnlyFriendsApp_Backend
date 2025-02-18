from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from ..database import get_db
from .services import get_similar_users, calculate_similarity
from ..auth.services import get_current_user
from ..auth.models import User
from .schemas import SimilarityResponse
from ..profile.models import Profile
from ..profile.services import get_user_profile_svc
from typing import List, Dict, Any

router = APIRouter(prefix="/similarity", tags=["Similarity"])

@router.post("/compute")
def compute_similarity(token:  str = Header(...) , db: Session = Depends(get_db)): # Explicitly define the return type
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
  
    calculate_similarity(db)
    return {"message": "User similarities computed successfully"}

@router.get("/{user_id}", response_model=List[SimilarityResponse])
def get_user_similarity(
    user_id: int, 
    token: str = Header(...),
    db: Session = Depends(get_db)): # Explicitly define the return type

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

    similar_users = get_similar_users(db, user_id)
    if not similar_users:
        raise HTTPException(status_code=404, detail="No similar users found")
    return [SimilarityResponse.model_validate(sim_user) for sim_user in similar_users]