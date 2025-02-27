# schemas.py
from pydantic import BaseModel
from typing import List, Optional

class SimilarityBase(BaseModel):
    user_id: int
    similar_user_id: int
    similarity_score: float

class SimilarityResponse(SimilarityBase):
    username: str
    profile_pic: Optional[str]
    interests: List[str]
    is_active: bool
    
    class Config:
        from_attributes = True
