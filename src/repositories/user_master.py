from datetime import datetime
from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import update
from sqlalchemy.orm import Session

from models.users.users import Users
from schemas.users.users import UserMasterSchema


def get_user_email(db: Session, user_email: str):
    try:
        return db.query(Users).filter(Users.email == user_email).first()

    except Exception as ex:
        db.close()
        raise ex


def get_single_user_id(db: Session, user_id: str):
    try:
        id_user = db.query(Users).filter(Users.user_id == user_id).first()
        return id_user

    except Exception as ex:
        db.close()
        raise ex


def get_user_id(db: Session, user_id: str, confi: bool = None):
    try:
        if confi:
            user_query = db.query(Users).filter(Users.user_id == user_id).first()

        else:
            user_query = (
                db.query(Users.user_id).filter(Users.user_id == user_id).first()
            )

        if not user_query:
            user_query = None

        return user_query

    except Exception as ex:
        db.close()
        raise ex


def get_single_user_email(db: Session, email: str):
    try:
        """Get single user email"""
        email = db.query(Users).filter(Users.email == email).first()
        if not email:
            email = None
        return email

    except Exception as ex:
        db.close()
        raise ex


def confirm_email_user(db: Session, user_id: str, confirm_email: bool):
    try:
        """Get single user email"""
        update_email = (
            update(Users)
            .where(Users.user_id == user_id)
            .values(confirm_email=confirm_email)
        )
        db.execute(update_email)
        user = db.query(Users).filter(Users.user_id == user_id).first()
        db.refresh(user)
        db.commit()
        return user

    except Exception as ex:
        db.close()
        raise ex


# POST
def create_user_master(db: Session, *, obj_in: UserMasterSchema):
    try:
        obj_in_data: Any = jsonable_encoder(obj_in)
        db_obj = Users(**obj_in_data)
        db_obj.load_date = datetime.utcnow()
        db_obj.update_date = datetime.utcnow()

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    except Exception as ex:
        db.rollback()
        db.close()
        raise ex


# PUT
def update_user_object(
    db: Session,
    *,
    obj_to_data: Users,
    obj_updater,
):
    try:
        # Update model class variable from requested fields
        obj_updater = obj_updater.dict(exclude_unset=True)
        for key, value in obj_updater.items():
            setattr(obj_to_data, key, value)
        db.add(obj_to_data)
        db.commit()
        db.refresh(obj_to_data)
        return obj_to_data

    except Exception as ex:
        db.rollback()
        db.close()
        raise ex


# DELETE
def delete_user_master_object(db: Session, user_id):
    try:
        """
        Crud method for delete a single user object
        """
        user_master = db.query(Users).filter(Users.user_id == user_id).first()
        db.query(Users).filter(Users.user_id == user_id).delete()
        db.commit()
        return user_master

    except Exception as ex:
        db.rollback()
        db.close()
        raise ex
