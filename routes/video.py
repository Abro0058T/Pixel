from fastapi import APIRouter, Depends, HTTPException

from models.video import Video
from schemas.video import VideoResponse

from core.db import get_db
from core.security import get_current_userinfo

from pymongo.database import Database

router = APIRouter()

@router.get("/all_videos", response_model=VideoResponse, tags=["video"])
def get_all_videos(current_user: dict = Depends(get_current_userinfo),
                    db:Database = Depends(get_db))->VideoResponse:
    """
    Get all videos
    """
    response:VideoResponse = db.videos.find({"user_email":current_user["sub"]})
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="No videos found")
    


@router.get("/video/{video_id}", response_model=VideoResponse, tags=["video"])
def get_video(current_user: dict = Depends(get_current_userinfo),
                video_id:str = None,
                db:Database = Depends(get_db))->VideoResponse:
    """
    Get a video by id
    """
    response:VideoResponse = db.videos.find_one({"prid":video_id, "user_email":current_user["sub"]})
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="Video not found")
    
