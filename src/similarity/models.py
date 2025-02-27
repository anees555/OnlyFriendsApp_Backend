# models.py
from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Similarity(Base):
    __tablename__ = "similarities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    similar_user_id = Column(Integer, ForeignKey("users.id"))
    similarity_score = Column(Float, nullable=False)
    is_active = Column(Boolean, default = True)

    user = relationship("auth.models.User", foreign_keys=[user_id])
    similar_user = relationship("auth.models.User", foreign_keys=[similar_user_id])

    