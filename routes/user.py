from fastapi import APIRouter,Depends

from models.user import User
from config.db import client
from schemas.user import UserRegisterData, RegisterResponse, UserLoginData, LoginResponse
from core.db import get_db
from core.security import get_hashed_password, verify_password, create_access_token

from pymongo.database import Database

router = APIRouter()

@router.post("/register", response_model=RegisterResponse, tags=["user"])
def register_user(user_data:UserRegisterData, 
                  db:Database=Depends(get_db))->RegisterResponse:
    """Register a new user"""

    user_exists = db.users.find_one({"email":user_data.email})
    if user_exists:
        return RegisterResponse(status="failure",
                                message="User already exists")
    else:
        if user_data.password == user_data.confirm_password:
            user_data.password = get_hashed_password(user_data.password)
            user = User(**user_data.model_dump())
            db.users.insert_one(user.model_dump())
            return RegisterResponse(status="success",
                                    message="User registered successfully")
        else:
            return RegisterResponse(status="failure",
                                    message="Password and confirm password do not match")



@router.post("/login")
def login_user(user_data:UserLoginData, 
               db:Database=Depends(get_db))->LoginResponse:
    """Login a user"""
    user = db.users.find_one({"email":user_data.email})
    if user:
        if verify_password(user_data.password, user["password"]):
            access_token = create_access_token(data={"sub":user_data.email})
            return LoginResponse(status="success",
                                message="User logged in successfully",
                                access_token=access_token)
        else:
            return LoginResponse(status="failure",
                                message="Incorrect password")
    else:
        return LoginResponse(status="failure",
                            message="User does not exist")