from fastapi import FastAPI
from .database import Base, engine
from .api import router
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind = engine)


# ✅ Apply CORS Middleware BEFORE including the router

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "v1/auth/token")

app = FastAPI(
    title="OnlyFriends App",
    version="0.1"
)
app.include_router(router)

# Define allowed frontend origins
origins = [
    "http://localhost:5173",  # Local dev frontend
    "https://onlyfriendsapp.netlify.app",  # Deployed frontend
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allows all origins, change it to your front-end URL for more security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Serve the profile pictures directory
app.mount("/profile_pictures", StaticFiles(directory="profile_pictures"), name="profile_pictures")

@app.get("/")
def root():
    return "Welcome to the OnlyFriends App"


