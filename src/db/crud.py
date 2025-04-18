# app/db/crud.py
from sqlalchemy.orm import Session
from .models import User

def get_user_by_uid(db: Session, uid: str):
    return db.query(User).filter(User.uid == uid).first()

def create_user(db: Session, uid: str, email: str):
    user = User(uid=uid, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

get_user_by_uid