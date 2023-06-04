from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import or_

from configs.database import create_session
from models import library
from schemas.library import LibraryRegistry


def get_book(db: Session, search_term: str):
    try:
        query = (
            db.query(library.Library)
            .filter(
                or_(
                    func.lower(library.Library.title).like(
                        func.lower(f"%{search_term}%")
                    ),
                    func.lower(library.Library.authors).like(
                        func.lower(f"%{search_term}%")
                    ),
                    func.lower(library.Library.categories).like(
                        func.lower(f"%{search_term}%")
                    ),
                    func.lower(library.Library.editor).like(
                        func.lower(f"%{search_term}%")
                    ),
                )
            )
            .all()
        )

        return query

    except Exception as ex:
        db.close()
        raise ex


def get_single_book_id(db: Session, id: int):
    try:
        book_id = db.query(library.Library).filter(library.Library.id == id).first()
        return book_id

    except Exception as ex:
        db.close()
        raise ex


def get_book_authors(db: Session, authors: str):
    try:
        book_authors = (
            db.query(library.Library).filter(library.Library.authors == authors).first()
        )
        return book_authors

    except Exception as ex:
        db.close()
        raise ex


def get_book_categories(db: Session, categories: str):
    try:
        book_categories = (
            db.query(library.Library)
            .filter(library.Library.categories == categories)
            .first()
        )
        return book_categories

    except Exception as ex:
        db.close()
        raise ex


def get_book_title(db: Session, title: str):
    try:
        book_title = (
            db.query(library.Library).filter(library.Library.title == title).first()
        )
        return book_title

    except Exception as ex:
        db.close()
        raise ex


def create_book_for_consult(data_list: list):
    db = create_session()
    for book in data_list:
        book_exists = get_book_title(db=db, title=book.get("title"))
        if not book_exists:
            create_book(db=db, obj_in=book)


# POST
def create_book(db: Session, *, obj_in: LibraryRegistry):
    try:
        obj_in_data: Any = jsonable_encoder(obj_in)
        db_obj = library.Library(**obj_in_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    except Exception as ex:
        db.rollback()
        db.close()
        raise ex


# PUT
def update_book(
    db: Session,
    *,
    obj_to_data: library.Library,
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
def delete_book_title(db: Session, id):
    try:
        """
        Crud method for delete a single user object
        """
        user_master = db.query(library.Library).filter(library.Library.id == id).first()
        db.query(library.Library).filter(library.Library.id == id).delete()
        db.commit()
        return user_master

    except Exception as ex:
        db.rollback()
        db.close()
        raise ex
