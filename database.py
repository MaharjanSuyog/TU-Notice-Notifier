import os

import redis
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


# POSTGRES CONNECTION
DATABASE_URL = os.getenv("POSTGRES_URL")
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_size=5,
    max_overflow=10,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


def getDB():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# REDIS CONNECTION
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    username=os.getenv("REDIS_USERNAME"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
)


def check_redis_connection():
    try:
        redis_client.ping()
        print("Redis connected successfully")
    except redis.ConnectionError as error:
        print(f"Redis connection failed: {error}")
