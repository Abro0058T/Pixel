from fastapi import APIRouter,Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from models.user import User
from config.db import client
from schemas.user import UserRegisterData, RegisterResponse, LoginResponse, UserInfoResponse
from core.db import get_db
from core.security import get_hashed_password, verify_password, create_access_token, get_current_userinfo

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



@router.post("/login", response_model=LoginResponse, tags=["user"])
def login_user(user_data:OAuth2PasswordRequestForm=Depends(), 
               db:Database=Depends(get_db))->LoginResponse:
    """Login a user"""
    user = db.users.find_one({"email":user_data.username})
    if user:
        if verify_password(user_data.password, user["password"]):
            access_token = create_access_token(data={"sub":user_data.username})
            return LoginResponse(status="success",
                                message="User logged in successfully",
                                access_token=access_token)
        else:
            return LoginResponse(status="failure",
                                message="Incorrect password")
    else:
        return LoginResponse(status="failure",
                            message="User does not exist")
    
@router.get("/user_info", response_model=UserInfoResponse, tags=["user"])
def get_user_info(current_user: dict = Depends(get_current_userinfo),
                    db:Database = Depends(get_db))->UserInfoResponse:
    """
    Get user information
    """
    user = db.users.find_one({"email":current_user["sub"]})
    if user:
        return UserInfoResponse(
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            aadhaar_no=user["aadhaar_no"],
            is_email_verified=user["is_email_verified"],
            is_aadhaar_verified=user["is_aadhaar_verified"],
            account_created_on=user["account_created_on"]
        )
    else:
        raise HTTPException(status_code=404, detail="User not found")