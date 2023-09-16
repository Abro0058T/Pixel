from pydantic import BaseModel
from typing import List

class VideoEditInfo(BaseModel):
    datetime: str
    edit_description: str


class Video(BaseModel):
    prid:int
    status: str
    link: str
    edit: List[VideoEditInfo]
    user_email: str