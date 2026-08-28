from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database import (
    SessionLocal,
    check_redis_connection,
    engine,
    get_db,
    initDB,
    redis_client,
)
from models import Notice
from scraper import run_scraper


@asynccontextmanager
async def lifespan(app: FastAPI):
    initDB()
    check_redis_connection()

    db = SessionLocal()
    try:
        run_scraper(redis_client=redis_client, db=db)
    finally:
        db.close()

    yield

    engine.dispose()
    print("Application shutting down")


app = FastAPI(title="TU NOTICE TRACKER", lifespan=lifespan)


@app.get("/")
def home():
    return {"message": "API is operational."}


@app.get("/notices")
def notices(db: Session = Depends(get_db)):
    return {"notices": db.query(Notice).order_by(Notice.notice_id.desc()).all()}
