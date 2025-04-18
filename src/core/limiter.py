# core/limiter.py
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import date
from src.db.database import get_db
from src.db import crud
from src.db import models

def get_or_create_usage(user_id: str, db: Session) -> models.UsageTracker:
    today = date.today()
    usage = (
        db.query(models.UsageTracker)
        .filter_by(user_id=user_id, date=today)
        .first()
    )
    if not usage:
        usage = models.UsageTracker(user_id=user_id, date=today)
        db.add(usage)
        db.commit()
        db.refresh(usage)
    return usage

def check_limits(user: models.User, action: str, db: Session = Depends(get_db)):
    plan_limits = {
        "free": {"pdf": 3, "chat": 20},
        "pro": {"pdf": 50, "chat": 500}
    }

    limits = plan_limits.get(user.plan, plan_limits["free"])
    usage = get_or_create_usage(user.id, db)

    if action == "pdf" and usage.pdf_count >= limits["pdf"]:
        raise HTTPException(status_code=429, detail="PDF upload limit reached today.")
    elif action == "chat" and usage.chat_count >= limits["chat"]:
        raise HTTPException(status_code=429, detail="Chat usage limit reached today.")


def increment_usage(user_id: str, action: str, db: Session):
    usage = get_or_create_usage(user_id, db)
    if action == "pdf":
        usage.pdf_count += 1
    elif action == "chat":
        usage.chat_count += 1
    db.commit()
