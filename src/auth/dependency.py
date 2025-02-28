# from fastapi import Request, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from datetime import datetime
# from ..database import get_db
# from .services import get_current_user
# from fastapi.security import OAuth2PasswordBearer
# import asyncio

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token")

# async def update_last_seen(request: Request, db: Session = Depends(get_db)):
#     # Extract token from the request headers
#     token = request.headers.get("Authorization")
    
#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Authorization header missing"
#         )
    
#     # Assuming you have a function that handles decoding the token
#     user = get_current_user(db, token)
    
#     if user:
#         user.last_seen = datetime.utcnow()
#         db.commit()
#         db.refresh(user)
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User not found"
#         )
