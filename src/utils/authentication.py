import logging
from datetime import datetime

import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext

from config import Settings
from core.database import create_session
from crud.register import get_single_register_user
from services.users_master import create_comfig_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid Token",
    headers={"WWW-Authenticate": "Bearer"},
)


async def very_token(token: str):
    """verify token from login"""
    method = very_token.__name__
    try:
        db = create_session()
        payload = jwt.decode(token, Settings.SECRET, algorithms=["HS256"])
        date = datetime.strptime(payload.get("date"), "%Y-%m-%d %H:%M:%S.%f")
        difference = datetime.now() - date
        if difference.total_seconds() > 86400:
            raise error

        user = get_single_register_user(db, email=payload.get("email"))
        if not user:
            raise error
        return user

    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise error
    finally:
        db.close()


def very_token_email(token: str):
    """verify token from email"""
    method = very_token_email.__name__
    try:
        db = create_session()
        payload = jwt.decode(token, Settings.SECRET, algorithms=["HS256"])
        date = datetime.strptime(payload.get("date"), "%Y-%m-%d %H:%M:%S.%f")
        difference = datetime.now() - date
        if difference.total_seconds() > 86400:
            raise error
        user = get_single_register_user(db, email=payload.get("email"))
        if not user:
            raise error
        create_comfig_email(user_id=user["user_id"], confirm_email=True)
        return user

    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    finally:
        db.close()


def verify_password(plain_password, database_hashed_password):
    return pwd_context.verify(plain_password, database_hashed_password)


def authenticate_user(email: str, password: str):
    db = create_session()
    user = get_single_register_user(db, email=email)
    if user and verify_password(password, user.RegisterModel.password):
        if not user.confirm_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not verifide",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    return False


def token_generator(email: str, password: str):
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = {
        "user_id": user.user_id,
        "email": user.RegisterModel.email,
        "date": str(datetime.utcnow()),
    }
    token = jwt.encode(token_data, Settings.SECRET, algorithm="HS256")
    return token
