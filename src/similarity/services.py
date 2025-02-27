from sqlalchemy.orm import Session
from ..profile.models import Profile, Interest, user_interest_association
from ..auth.models import User
from .models import Similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math

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

    existing_similarities = db.query(Similarity).all()
    existing_similarity_map = {(sim.user_id, sim.similar_user_id): sim.is_active for sim in existing_similarities}

    db.query(Similarity).delete()
    for i, user_id in enumerate(user_ids):
        for j, similar_user_id in enumerate(user_ids):
            if user_id != similar_user_id:
                similarity_score = float(similarity_matrix[i, j])
                is_active = existing_similarity_map.get((user_id, similar_user_id), True)

                similarity_entry = Similarity(
                    user_id=user_id,
                    similar_user_id=similar_user_id,
                    similarity_score=similarity_score,
                    is_active =  is_active

                )
                db.add(similarity_entry)
    db.commit()

def get_similar_users(db: Session, user_id: int):
    similar_users = db.query(Similarity).filter(Similarity.user_id == user_id, Similarity.similarity_score > 0.1).order_by(Similarity.similarity_score.desc()).all()
    result = []
    for similar_user in similar_users:
        profile = db.query(Profile).filter(Profile.user_id == similar_user.similar_user_id).first()
        if profile:
            interests = db.query(Interest).join(user_interest_association).filter(user_interest_association.c.user_id == similar_user.similar_user_id).all()
            interest_names = [interest.name for interest in interests]
            result.append({
                "user_id": similar_user.user_id,
                "similar_user_id": similar_user.similar_user_id,
                "username": profile.user.username,
                "profile_pic": profile.profile_pic,
                "similarity_score": math.ceil(similar_user.similarity_score * 100),
                "interests": interest_names,
                "is_active": similar_user.is_active
            })
    return result                           