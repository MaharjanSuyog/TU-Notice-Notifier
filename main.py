from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import check_redis_connection, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # init_db()
    check_redis_connection()

    yield

    engine.dispose()


app = FastAPI(title="TU NOTICE TRACKER", lifespan=lifespan)


@app.get("/")
def home():
    return {"message": "API is operational."}
