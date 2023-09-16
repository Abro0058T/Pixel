from fastapi import APIRouter

from models.user import User
from config.db import client
from schemas.user import userEntity ,usersEntity

user=APIRouter()

@user.get('/')
async def find_all_user():
    print(client.local.user.find())
    print(usersEntity(client.local.user.find()))
    return usersEntity(client.local.user.find())

@user.post("/login")
async def login():
    return ("login")

@user.get("/allVideo")
def find_all_Video():
    return ("All video")
    
@user.get("/video/{id}")
def find_video(id=int  ):
    return (id,"id")
@user.post("/video/edit/{id}")
def edit_video():
    return("Video edited",id)


