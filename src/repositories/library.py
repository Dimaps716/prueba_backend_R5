from datetime import datetime
from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from models import library
from schemas.library import LibraryRegistry


def get_book(db: Session, search_term: str):
    try:
        return (
            db.query(library.Library)
            .filter(
                library.Library.title.ilike(f"%{search_term}%"),
                library.Library.subtitle.ilike(f"%{search_term}%"),
                library.Library.authors.ilike(f"%{search_term}%"),
                library.Library.categories.ilike(f"%{search_term}%"),
                library.Library.editor.ilike(f"%{search_term}%"),
                library.Library.description.ilike(f"%{search_term}%"),
            )
            .all()
        )

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
            db.query(library.Library)
            .filter(library.Library.book_title == title)
            .first()
        )
        return book_title

    except Exception as ex:
        db.close()
        raise ex


# POST
def create_book(db: Session, *, obj_in: LibraryRegistry):
    try:
        obj_in_data: Any = jsonable_encoder(obj_in)
        db_obj = library.Library(**obj_in_data)
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
