from fastapi import APIRouter
from routes import user

router = APIRouter()
router.include_router(user.router)
