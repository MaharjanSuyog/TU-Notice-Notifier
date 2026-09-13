from contextlib import asynccontextmanager

from database import (
    check_redis_connection,
    engine,
    initDB,
)
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, notices, unsubscribe
from scheduler import start_scheduler, stop_scheduler
from utils.mail import send_notices_email

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    initDB()
    check_redis_connection()
    start_scheduler()

    yield

    stop_scheduler()
    engine.dispose()
    print("Application shutting down")


app = FastAPI(title="TU NOTICE TRACKER", lifespan=lifespan, redirect_slashes=False)


@app.get("/")
def home():
    return {"message": "API is operational."}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notices.router)
app.include_router(auth.router)
# app.include_router(unsubscribe.router)
# @app.get("/web")
# def web():
#     httpx.post(
#         "***REMOVED***",
#         json={
#             "embeds": [
#                 {
#                     "title": "weeeeee",
#                     "url": "https://localhost:3000",
#                     "color": "3447003",
#                 }
#             ]
#         },
#     )


@app.get("/test")
async def test():
    return await send_notices_email(
        "suyogmaharjan38@gmail.com",
        [{"title": "B.Sc. CSIT Result Published", "link": "https://youtube.com"}],
        "test",
    )
