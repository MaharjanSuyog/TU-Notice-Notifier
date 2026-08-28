from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import SessionLocal, check_redis_connection, engine, initDB, redis_client
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
