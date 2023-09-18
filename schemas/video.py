from pydantic import BaseModel
from typing import List

class ImageInfo(BaseModel):
    # id: int
    url: str
    tags: List[str] = None


class VideoEditInfo(BaseModel):
    datetime: str
    language: str
    voice_gender:str
    ImageList: List[ImageInfo]
    # text_list: List[str] = None


class VideoResponse(BaseModel):
    prid:int
    status: str
    url: str
    edit_history: List[VideoEditInfo] = None
    user_email: str
    datetime: str
    ministry_name: str
    heading: str
    images: List[ImageInfo] = None
    text_list: List[str] = None
    language: str
    release_language:List[str]=None


class VideoListResponse(BaseModel):
    videos:List[VideoResponse]


class UserVideoStats(BaseModel):
    total_videos: int
    total_accepted: int
    total_rejected: int
    total_pending: int