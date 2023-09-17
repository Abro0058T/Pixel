from fastapi import APIRouter, Depends, HTTPException

from models.video import Video
from schemas.video import VideoListResponse, VideoResponse, UserVideoStats

from core.db import get_db
from core.security import get_current_userinfo

from pymongo.database import Database

router = APIRouter()

@router.get("/all_videos", response_model=VideoListResponse, tags=["video"])
def get_all_videos(current_user: dict = Depends(get_current_userinfo),
                    db:Database = Depends(get_db))->VideoListResponse:
    """
    Get all videos
    """
    response:VideoListResponse = db.videos.find({"user_email":current_user["sub"]})
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="No videos found")
    


@router.get("/video/{prid}", response_model=Video, tags=["video"])
def get_video(current_user: dict = Depends(get_current_userinfo),
                prid:int = None,
                db:Database = Depends(get_db))->VideoResponse:
    """
    Get a video by id
    """
    response:VideoResponse = db.videos.find_one({"prid":prid, "user_email":current_user["sub"]})
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="Video not found")


@router.get("/video/stats", tags=["video"], response_model=UserVideoStats)
def get_video_stats(current_user: dict = Depends(get_current_userinfo),
                    db:Database = Depends(get_db))->UserVideoStats:
    """
    Get video stats for user
    """
    total_videos = db.videos.count_documents({"user_email":current_user["sub"]})
    total_accepted = db.videos.count_documents({"user_email":current_user["sub"], "status":"accepted"})
    total_rejected = db.videos.count_documents({"user_email":current_user["sub"], "status":"rejected"})
    total_pending = db.videos.count_documents({"user_email":current_user["sub"], "status":"pending"})
    return UserVideoStats(total_videos=total_videos, total_accepted=total_accepted, total_rejected=total_rejected, total_pending=total_pending)