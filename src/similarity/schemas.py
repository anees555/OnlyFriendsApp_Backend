# schemas.py
from pydantic import BaseModel
from typing import List

class SimilarityBase(BaseModel):
    user_id: int
    similar_user_id: int
    similarity_score: float

class SimilarityResponse(SimilarityBase):
    class Config:
        from_attributes = True
