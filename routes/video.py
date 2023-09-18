from fastapi import APIRouter, Depends, HTTPException

from models.video import Video
from schemas.video import VideoListResponse, VideoResponse
from schemas.video import VideoEditInfo, UserVideoStats

from core.db import get_db
from core.security import get_current_userinfo

from pymongo.database import Database

import asyncio
# from services.mainVideo2 import generate_video_task

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


# /video/{prid}/edit for ediing video call 
# text_list[] -same array as in data base
# image[] updated array
#video(image,text) 
# 
@router.post("/video/{prid}/edit", response_model=VideoResponse, tags=["video"])
def edit_video(prid:int,
               edit_info:VideoEditInfo,
                current_user: dict = Depends(get_current_userinfo),
                db:Database = Depends(get_db))->VideoResponse:
    """
    Edit a video
    """
    # inserting edit_info into edit_history of video with give prid
    db.videos.update_one({"prid":prid, "user_email":current_user["sub"]},
                          {"$push":{"edit_history":edit_info.model_dump()}})
    # make video status again to 'Generating' and url to ""
    db.videos.update_one({"prid":prid, "user_email":current_user["sub"]},
                            {"$set":{"status":"Generating", "url":""}})
    
    # starts a background task to generate video
    # (work in progress)
    # asyncio.create_task(generate_video_task())

    # return the updated video response
    edited_video_response:VideoResponse = db.videos.find_one({"prid":prid, "user_email":current_user["sub"]})
    return edited_video_response

