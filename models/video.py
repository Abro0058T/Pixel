from pydantic import BaseModel
from typing import List
from datetime import datetime

class ImageInfo(BaseModel):
    # id: int
    url: str
    tags: List[str] = None


class VideoEditInfo(BaseModel):
    datetime: str
    language: str
    voice_gender:str
    ImageList: List[ImageInfo] = None
    # text_list: List[str] = None


class Video(BaseModel):
    prid:int
    status: str="Generating"
    url: str = None
    edit_history: List[VideoEditInfo] = None
    user_email: str =None
    datetime: str =datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    ministry_name: str = None
    heading: str =  None
    images: List[ImageInfo] = None
    text_list: List[str] = None
    language: str="English"
    release_language:List[str]=None
