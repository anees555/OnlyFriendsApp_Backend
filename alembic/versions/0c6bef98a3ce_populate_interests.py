"""populate interests

Revision ID: 0c6bef98a3ce
Revises: 3a6281d81132
Create Date: 2025-02-12 01:25:55.836589

"""
from typing import Sequence, Union
import sqlalchemy as sa
from sqlalchemy.orm import Session
from alembic import op
from src.profile.models import Interest


# revision identifiers, used by Alembic.
revision: str = '0c6bef98a3ce'
down_revision: Union[str, None] = '3a6281d81132'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Predefined list of interests
interests_list = [
    "Reading", "Traveling", "Cooking", "Sports", "Music", "Movies", "Gaming",
    "Fitness", "Art", "Photography", "Writing", "Dancing", "Gardening",
    "Hiking", "Cycling", "Yoga", "Meditation", "Singing",
    "Technology", "Fashion", "Pet", "Nature", "Science",
    "History", "Languages", "Coffee", "Tea", "Camping", "Coding"
]


def upgrade() -> None:
    pass
    

def downgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)
    try:
        session.query(Interest).delete()
        session.commit()
        print("interest removed successfully.")
    except Exception as e:
        session.rollback()
        print(f"error removing interests: {e}")
    finally:
        session.close()
    
