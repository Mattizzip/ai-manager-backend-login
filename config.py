import os
from dotenv import load_dotenv
import redis

load_dotenv()

class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = r'postgresql://postgres:0@localhost:5432/ai-manager-db'
    
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True
    SESSION_PERMANENT = False
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
    SESSION_COOKIE_HTTPONLY=False,
    SESSION_COOKIE_SECURE=False, 