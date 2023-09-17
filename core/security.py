from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError, ExpiredSignatureError
import bcrypt
from core.settings import Settings

from datetime import datetime, timedelta


reusesable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/login",
    scheme_name="JWT"
)

def get_hashed_password(plain_text_password: str)->str:
    """
    Hash a password for storing.
    """
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())


def verify_password(plain_text_password: str, hashed_password: str)->bool:
    """
    Verify a stored password against one provided by user
    """
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict, expires_delta: int = Settings.JWT_ACCESS_EXPIRE_MINUTES)->str:
    """
    Create a new access token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Settings.JWT_SECRET_KEY, algorithm=Settings.JWT_ALGORITHM)
    return encoded_jwt

def get_current_userinfo(token: str = Depends(reusesable_oauth2))->dict:
    """
    Get the current user info
    """
    print(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials/Token expired",
        headers={"WWW-Authenticate":"Bearer"}
    )
    payload:dict = {}
    try:
        payload = jwt.decode(token, Settings.JWT_SECRET_KEY, Settings.JWT_ALGORITHM)
        email: str = payload.get("sub")
        if email is None:
            print("email is none")
            raise credentials_exception
    except JWTError as e2:
        raise credentials_exception
    return payload