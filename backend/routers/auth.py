import json
import os
import secrets
import urllib.parse
from typing import Annotated

import httpx
from database import get_db, redis_client
from dependencies import get_current_subscriber
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from models import Subscriber
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
FRONTEND_URL = os.getenv("FRONTEND_URL")

GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"

SESSION_TTL = 60 * 60 * 24 * 12
IS_PROD = os.getenv("ENV", "development") == "production"


def _issue_session(sub: Subscriber, redirect: RedirectResponse):
    session_id = secrets.token_urlsafe(32)
    redis_client.setex(
        f"session:{session_id}",
        SESSION_TTL,
        json.dumps({"subscriber_id": sub.id}, default=str),
    )

    csrf_token = secrets.token_urlsafe(32)
    redis_client.setex(f"csrf:{session_id}", SESSION_TTL, csrf_token)

    redirect.set_cookie(
        "session_id",
        session_id,
        httponly=True,
        secure=IS_PROD,
        samesite="lax",
        max_age=SESSION_TTL,
    )

    redirect.set_cookie(
        "csrf_token",
        csrf_token,
        httponly=False,
        secure=IS_PROD,
        samesite="lax",
        max_age=SESSION_TTL,
    )


class GoogleAuthPayload(BaseModel):
    credential: str


@router.get("/google/login")
def start_google_login():
    state = secrets.token_urlsafe(24)

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email",
        "state": state,
        "prompt": "select_account",
    }

    redirect = RedirectResponse(
        f"{GOOGLE_AUTH_ENDPOINT}?{urllib.parse.urlencode(params)}"
    )

    redirect.set_cookie(
        "oauth_state", state, httponly=True, secure=IS_PROD, samesite="lax", max_age=300
    )
    return redirect


@router.get("/google/callback")
async def google_callback(
    code: str,
    state: str,
    db: Annotated[Session, Depends(get_db)],
    oauth_state: Annotated[str | None, Cookie()] = None,
):
    if not oauth_state or state != oauth_state:
        raise HTTPException(status_code=400, detail="Invalid OAuth State")

    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            GOOGLE_TOKEN_ENDPOINT,
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
    if token_res.status_code != 200:
        raise HTTPException(
            status_code=502, detail=f"Google token exchange failed: {token_res.text}"
        )
    token_res.raise_for_status()
    tokens = token_res.json()

    claims = google_id_token.verify_oauth2_token(
        tokens["id_token"], google_requests.Request(), GOOGLE_CLIENT_ID
    )

    if claims.get("iss") not in ("accounts.google.com", "https://accounts.google.com"):
        raise HTTPException(status_code=401, detail="Unexpected Token Issuer")

    if not claims.get("email_verified"):
        raise HTTPException(status_code=401, detail="Google email not verified")

    email = claims["email"]
    google_id = claims["sub"]

    sub = db.query(Subscriber).filter_by(google_id=google_id).first()
    if sub is None:
        sub = Subscriber(email=email, google_id=google_id, status="active")
        db.add(sub)
    elif sub.email != email:
        sub.email = email
    db.commit()
    db.refresh(sub)

    redirect = RedirectResponse(FRONTEND_URL)
    _issue_session(sub, redirect)
    redirect.delete_cookie("oauth_state")
    return redirect


@router.get("/me")
def get_current_session(sub: Annotated[Subscriber, Depends(get_current_subscriber)]):
    return {"email": sub.email, "status": sub.status, "is_admin": sub.is_admin}


@router.post("/logout")
def logout(response: Response, session_id: str | None = Cookie(default=None)):
    if session_id:
        redis_client.delete(f"session:{session_id}")
        redis_client.delete(f"csrf:{session_id}")
    response.delete_cookie("session_id")
    response.delete_cookie("csrf_token")
    return {"status": "loggedout"}
