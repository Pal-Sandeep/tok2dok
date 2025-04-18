# app/api/deps.py

from fastapi import Depends, HTTPException, status, Request
from firebase_admin import auth as firebase_auth, credentials, initialize_app
from firebase_admin._auth_utils import InvalidIdTokenError
from functools import lru_cache
import firebase_admin

from src.db import crud, database, models

# Initialize Firebase only once
@lru_cache()
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("src/firebase_service_account.json")  # download from Firebase Console
        initialize_app(cred)

init_firebase()

def get_current_user(request: Request, db=Depends(database.get_db)) -> models.User:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = auth_header.split(" ")[1]
    try:
        decoded = firebase_auth.verify_id_token(token)
        uid = decoded["uid"]
        email = decoded.get("email")

        # Fetch or create local DB user
        user = crud.get_user_by_uid(db, uid)
        if not user:
            user = crud.create_user(db, uid=uid, email=email)

        return user

    except InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")
