from fastapi import APIRouter
from .auth.views import router as auth_router
from .profile.views import router as profile_router
from .post.views import router as post_router

router  = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(profile_router)
router.include_router(post_router)
