import json
from typing import Annotated

from database import get_db, redis_client
from fastapi import Cookie, Depends, HTTPException
from models import Subscriber
from sqlalchemy.orm import Session


def get_current_subscriber(
    session_id: Annotated[str | None, Cookie()] = None,
    db: Annotated[Session, Depends(get_db)] = None,
) -> Subscriber:
    if not session_id:
        raise HTTPException(status_code=401, detail="Not Authenticated")

    raw = redis_client.get(f"session:{session_id}")
    if not raw:
        raise HTTPException(
            status_code=401, detail="Session Expired, Please sign in again"
        )

    data = json.loads(raw)
    sub = db.get(Subscriber, data["subscriber_id"])

    if sub is None:
        raise HTTPException(status_code=401, detail="Invalid Session")

    return sub
