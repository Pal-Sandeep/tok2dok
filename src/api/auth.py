# app/api/auth.py

import logging
from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from firebase_admin import auth as firebase_auth
import uvicorn
from src.db import crud, database
from src.db.models import User

router = APIRouter()

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)
logger.info("API is starting up")
logger.info(uvicorn.Config.asgi_version)

class TokenRequest(BaseModel):
    id_token: str

@router.post("/login")
def login_or_signup(token_data: TokenRequest, db=Depends(database.get_db)):
    try:
        logger.debug(token_data.id_token, 'id_tokenn.......................................')
        logger.info(token_data.id_token, 'id_tokenn.......................................')
        decoded_token = firebase_auth.verify_id_token(token_data.id_token)
        uid = decoded_token["uid"]
        email = decoded_token.get("email")

        # Check if user exists
        user = crud.get_user_by_uid(db, uid)
        if not user:
            # Create new user
            user = crud.create_user(db, uid=uid, email=email)

        return {
            "id": user.id,
            "uid": user.uid,
            "email": user.email,
            "message": "Login successful"
        }

    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid Firebase ID token")
