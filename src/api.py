from fastapi import APIRouter
from .auth.views import router as auth_router
from .profile.views import router as profile_router
from .post.views import router as post_router
from .similarity.views import router as simi_router
from .Friends_connect.views import router as friends_router

router  = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(profile_router)
router.include_router(post_router)
router.include_router(simi_router)
router.include_router(friends_router)
