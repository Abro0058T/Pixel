from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_EXPIRE_MINUTES = int(os.getenv('JWT_ACCESS_EXPIRE_MINUTES'))