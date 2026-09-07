from contextlib import asynccontextmanager

from database import (
    check_redis_connection,
    engine,
    initDB,
)
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, notices
from scheduler import start_scheduler, stop_scheduler

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

# @app.get("/web")
# def web():
#     httpx.post(
#         "https://discord.com/api/webhooks/1545747401925722202/VYMcNe_POvTsloqaDTcPznVxlr4xGnA5C7w0GNpr5QUWQz-yZB0naDA_DCh3NhSzMm2C",
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
