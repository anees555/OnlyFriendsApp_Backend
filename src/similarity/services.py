from sqlalchemy.orm import Session
from ..profile.models import Profile, Interest, user_interest_association
from ..auth.models import User
from .models import Similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(db: Session):
    users = db.query(User).all()
    user_interests = {}
    
    for user in users:
        interests = db.query(Interest).join(user_interest_association).filter(user_interest_association.c.user_id == user.id).all()
        user_interests[user.id] = " ".join([interest.name for interest in interests])

    user_ids = list(user_interests.keys())
    interest_texts = list(user_interests.values())
    print(f"{user_ids}: {interest_texts}")

    vectorizer = TfidfVectorizer()
    interest_matrix = vectorizer.fit_transform(interest_texts)
    similarity_matrix = cosine_similarity(interest_matrix)

    db.query(Similarity).delete()
    for i, user_id in enumerate(user_ids):
        for j, similar_user_id in enumerate(user_ids):
            if user_id != similar_user_id:
                similarity_score = float(similarity_matrix[i, j])
                similarity_entry = Similarity(
                    user_id=user_id,
                    similar_user_id=similar_user_id,
                    similarity_score=similarity_score
                )
                db.add(similarity_entry)
    db.commit()

def get_similar_users(db: Session, user_id: int):
    similar_users = db.query(Similarity).filter(Similarity.user_id == user_id).order_by(Similarity.similarity_score.desc()).all()
    result = []
    for similar_user in similar_users:
        profile = db.query(Profile).filter(Profile.user_id == similar_user.similar_user_id).first()
        if profile:
            result.append({
                "user_id": similar_user.similar_user_id,
                "similar_user_id": similar_user.user_id,
                "username": profile.user.username,
                "profile_pic": profile.profile_pic,
                "similarity_score": similar_user.similarity_score
            })
    return result