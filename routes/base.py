from fastapi import APIRouter

from routes import user
from routes import video

router = APIRouter()
router.include_router(user.router)
router.include_router(video.router)
