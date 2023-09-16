from pydantic import BaseModel
from typing import List

class VideoEditInfo(BaseModel):
    """
    Model for video edit info
    """
    datetime: str
    edit_description: str


class VideoResponse(BaseModel):
    """
    Response model for video
    """
    prid:int
    status: str
    link: str
    edit: List[VideoEditInfo]
    user_email: str