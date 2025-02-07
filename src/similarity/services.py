from sqlalchemy.orm import Session
from ..profile.models import Profile
from .models import Similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(db:Session):
    profiles = db.query(Profile).all()
    user_interests = {profile.user_id : profile.interests for profile in profiles}

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
    return db.query(Similarity).filter(Similarity.user_id == user_id).order_by(Similarity.similarity_score.desc()).all()
