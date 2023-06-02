import logging
from typing import Any

from fastapi import HTTPException, status

from configs.database import create_session
from repositories.user_master import (
    confirm_email_user,
    create_user_master,
    delete_user_master_object,
    get_single_user_email,
    get_single_user_id,
    get_user_id,
    update_user_object,
)
from schemas.users.users import UpdateUserMasterSchema, UserMasterSchema

NotItem = "Item not found"


def get_user_by_id(user_id: str):
    method = get_user_by_id.__name__
    """
    Get a single user in the database

    Args:
        user_id (str): User ID

    Returns:
        dict: user master
    """
    try:
        db = create_session()

        get_single_user = get_single_user_id(db, user_id=user_id)
        if not get_single_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NotItem)
        return get_single_user
    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"error {method}")
    finally:
        db.close()


def get_users_by_email(email: str) -> Any:
    method = get_users_by_email.__name__
    """
    Get single user email

    Args:
        email (str):

    Returns:
        dict: user master
    """
    try:
        db = create_session()

        get_single_user = get_single_user_email(db, email=email)
        if not get_single_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="email not exits"
            )
        return get_single_user
    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"error get users by email,{method}"
        )
    finally:
        db.close()


def create_user(form_in: UserMasterSchema) -> dict:
    method = get_users_by_email.__name__

    """
    create user in  database
    Body:
        form_in: is a UserMasterSchema model

    Returns:
        dict: user master
    """
    try:
        db = create_session()

        return create_user_master(db, obj_in=form_in)

    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"error create form user, {method}"
        )
    finally:
        db.close()


def create_comfig_email(user_id: str, confirm_email: bool):
    method = create_comfig_email.__name__

    try:
        db = create_session()

        return confirm_email_user(db, user_id=user_id, confirm_email=confirm_email)

    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"error confirm email, {method}"
        )
    finally:
        db.close()


def update_user(user_id: str, obj_updater: UpdateUserMasterSchema):
    method = update_user.__name__

    """
    Update a single user type record in the database

    :param user_id: The user ID to update
    :type user_id: str
    :param obj_updater: is a UpdateUserMasterSchema model
    :type obj_updater: UpdateUserMasterSchema
    :return: A single user type record in the database
    """
    try:
        db = create_session()

        db_obj = get_user_id(db, user_id=user_id)
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NotItem)

        return update_user_object(db, obj_to_data=db_obj, obj_updater=obj_updater)
    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"error update user, {method}"
        )
    finally:
        db.close()


def delete_user_master(user_id: str):
    method = delete_user_master.__name__

    """
    Delete a single user record in the database

    Args:
        user_id (str): User ID

    Returns:
        dict: user master
    """
    try:
        db = create_session()

        db_obj = get_single_user_id(db, user_id=user_id)
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NotItem)
        db_user = delete_user_master_object(db=db, user_id=user_id)
        return db_user
    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(
            status.HTTP_424_FAILED_DEPENDENCY, detail=f"error delete user, {method}"
        )
    finally:
        db.close()
