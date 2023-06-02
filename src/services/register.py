import logging
import uuid
from typing import Any
from passlib.context import CryptContext

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from core.database import create_session
from crud.register import (
    create_register,
    get_register_first_name,
    get_single_register_email,
    update_register_object,
)
from crud.user_master import create_user_master
from enums.user_type import UserTypes
from schemas.users.user_register import UpdateRegistry, UserRegistry

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_registry(first_name: str, user_type: int):
    method = get_registry.__name__
    try:
        db = create_session()
        return get_register_first_name(db, first_name=first_name, user_type=user_type)
    except Exception as ex:
        logging.error(f"Error when execute {method}: {ex}")
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail={"message": f"Error when execute method {method}: {ex}"},
        )
    finally:
        db.close()


def get_registry_by_email(email: str) -> Any:
    method = get_registry_by_email.__name__

    try:
        db = create_session()

        et_registry = get_single_register_email(db, email=email)
        if not et_registry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="email not exits"
            )
        return et_registry
    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"error get registry by email,{method}"
        )
    finally:
        db.close()


def create_registry(form_in: UserRegistry):
    method = create_registry.__name__

    try:
        db = create_session()

        form_in.password = pwd_context.hash(form_in.password)

        get_register_email = get_single_register_email(db, email=form_in.email)

        if get_register_email:
            return JSONResponse(
                content={"details": "User already exist"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        register = create_register(db, obj_in=form_in)

        create_user = {
            "user_id": uuid.uuid4(),
            "user_type_id": UserTypes.user.value,
            "first_name": register.first_name,
            "last_name": register.last_name,
            "email": register.email,
            "confirm_email": False,
        }
        create_user_master(db=db, obj_in=create_user)

        return create_user

    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"error create register, {method}"
        )
    finally:
        db.close()


def updates_registry(email: str, obj_updater: UpdateRegistry):
    method = updates_registry.__name__

    try:
        db = create_session()

        db_obj = get_single_register_email(db, email=email)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"register not exits, {method}",
            )

        return update_register_object(db, obj_to_data=db_obj, obj_updater=obj_updater)
    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"error update user, {method}"
        )
    finally:
        db.close()
