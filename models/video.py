from pydantic import BaseModel
from typing import List


class ImageInfo(BaseModel):
    id: int
    url: str
    tags: List[str]


class VideoEditInfo(BaseModel):
    datetime: str
    language: str
    voice_gender:str
    ImageList: List[ImageInfo]


class Video(BaseModel):
    prid:int
    status: str
    url: str
    edit_history: List[VideoEditInfo] = None
    user_email: str
    datetime: str
    ministry_name: str
    heading: str
    images: List[ImageInfo] = None
    language: str
