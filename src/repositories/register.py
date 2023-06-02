from typing import Optional, Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from models.users.user_register import RegisterModel
from models.users.users import Users
from schemas.users.user_register import UserRegistry


def get_single_register_user(db: Session, email: str):
    try:
        obj = (
            db.query(
                RegisterModel,
                Users.confirm_email,
                Users.user_id,
            )
            .join(RegisterModel, Users.email == RegisterModel.email)
            .filter(RegisterModel.email == email)
            .first()
        )
        if not obj:
            return None
        return obj

    except Exception as ex:
        db.close()
        raise ex


def get_all_register_objects(
    db: Session, skip: Optional[int] = None, limit: Optional[int] = None
):
    try:
        return db.query(RegisterModel).offset(skip).limit(limit).all()
    except Exception as ex:
        db.close()
        raise ex


def get_single_register_object(db: Session, id: int):
    try:
        return db.query(RegisterModel).filter(RegisterModel.id == id).first()
    except Exception as ex:
        db.close()
        raise ex


def get_single_register_email(db: Session, email: str):
    try:
        email = (
            db.query(
                RegisterModel,
            )
            .filter(RegisterModel.email == email)
            .first()
        )
        if not email:
            email = None
        return email
    except Exception as ex:
        db.close()
        raise ex


def get_register_first_name(db: Session, first_name: str, user_type: int):
    try:
        first_name = (
            db.query(RegisterModel, Users.user_type_id)
            .join(RegisterModel, Users.email == RegisterModel.email)
            .filter(
                RegisterModel.first_name == first_name, Users.user_type_id == user_type
            )
            .all()
        )
        return first_name
    except Exception as ex:
        db.close()
        raise ex


# POST


def create_register(db: Session, *, obj_in: UserRegistry):
    try:
        obj_in_data: Any = jsonable_encoder(obj_in)
        db_obj = RegisterModel(**obj_in_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except Exception as ex:
        db.rollback()
        db.close()
        raise ex


# UPDATE
def update_register_object(
    db: Session,
    *,
    obj_to_data: RegisterModel,
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
def delete_register_object(db: Session, id):
    """
    Crud method for delete a single object
    """
    try:
        register = db.query(RegisterModel).filter(RegisterModel.id == id).first()
        db.query(RegisterModel).filter(RegisterModel.id == id).delete()
        db.commit()
        return register
    except Exception as ex:
        db.rollback()
        db.close()
        raise ex


def delete_register_by_email(db: Session, email):
    """
    Crud method for delete a single object
    """
    try:
        register = db.query(RegisterModel).filter(RegisterModel.email == email).first()
        db.query(RegisterModel).filter(RegisterModel.email == email).delete()
        db.commit()
        return register
    except Exception as ex:
        db.rollback()
        db.close()
        raise ex
