from pydantic import BaseModel


class UserLoginData(BaseModel):
    """
    User login data
    """
    email: str
    password: str


class LoginResponse(BaseModel):
    """
    Response model for user login
    """
    status: str
    message: str
    access_token: str = None


class UserRegisterData(BaseModel):
    """
    User registration data
    """
    first_name: str
    last_name: str
    email: str
    password: str
    confirm_password:str
    aadhaar_no: str


class RegisterResponse(BaseModel):
    """
    Response model for user registration
    """
    status: str
    message: str