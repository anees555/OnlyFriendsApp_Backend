# from sqlalchemy import Column, Date, DateTime, Integer, String, ForeignKey


# from ..database import Base
# from datetime import datetime
# from sqlalchemy.orm  import relationship

# class FriendRequest(Base):
#     __tablename__ = "friend_requests"
    
#     id = Column(Integer, primary_key = True, index = True)
#     sender_id = Column(Integer, ForeignKey("users.id"))
#     receiver_id = Column(Integer, ForeignKey("users.id"))
#     status = Column(String, default = "pending")
#     created_at = Column(DateTime, default = datetime.utcnow())

#     sender = relationship("User", back_populates  = "sent_requests", foreign_keys = [sender_id])
#     receiver = relationship("User", back_populates = "received_requests", foreign_keys = [receiver_id])

    


