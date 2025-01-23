from fastapi import FastAPI
from .database import Base, engine
from .api import router
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind = engine)

app = FastAPI(
    title="OnlyFriends App",
    version="0.1"
)
app.include_router(router)


# Serve the profile pictures directory
app.mount("/profile_pictures", StaticFiles(directory="profile_pictures"), name="profile_pictures")

@app.get("/")
def root():
    return "Welcome to the OnlyFriends App"




