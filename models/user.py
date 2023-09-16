from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    aadhaar_no: str
    is_email_verified: bool = False
    is_aadhaar_verified: bool = False
    account_created_on: str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
