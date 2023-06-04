import logging
import queue
import threading
from typing import Any

from fastapi.responses import JSONResponse
from fastapi import HTTPException, status

from clients import google_books, books_open_library, books_library_of_congress

from configs.database import create_session
from repositories.library import (
    create_book,
    delete_book_title,
    get_book,
    get_book_authors,
    get_book_categories,
    get_book_title,
    get_single_book_id,
    update_book,
)
from schemas.library import LibraryRegistry, UpdateLibrary

NotItem = "Item not found"


def get_books_db(search_term: str):
    """
    Get a single book in the database

    Args:
        search_term (str)

    Returns:
        dict: book
    """
    method = get_books_db.__name__
    try:
        db = create_session()

        get_books = get_book(db, search_term.rstrip())
        if get_books:
            # Devolver los resultados de la base de datos
            list_book = []
            for book in get_books:
                list_book.append(
                    {
                        "id": book.id,
                        "title": book.title,
                        "subtitle": book.subtitle,
                        "authors": book.authors,
                        "categories": book.categories,
                        "editor": book.editor,
                        "description": book.description,
                        "image": book.image,
                    }
                )
            data = {"source": "database", "data": list_book}
            return data

        else:
            threads = []
            result = queue.Queue()

            google_books_thread = threading.Thread(
                target=google_books.search_books_in_google_api,
                args=(search_term, result),
                daemon=True,
            )
            threads.append(google_books_thread)

            open_library_thread = threading.Thread(
                target=books_open_library.search_books_open_library,
                args=(search_term, result),
                daemon=True,
            )
            threads.append(open_library_thread)

            library_of_congress_thread = threading.Thread(
                target=books_library_of_congress.search_books_library_of_congress,
                args=(search_term, result),
                daemon=True,
            )
            threads.append(library_of_congress_thread)

            value_data = []
            for star in threads:
                star.start()
                value_data.append(result.get())
                star.join(timeout=0.2)
                result.task_done()

            return value_data

    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"error {method}")

    finally:
        db.close()


def single_book(
    id: int = None, authors: str = None, categories: str = None, title: str = None
) -> Any:
    method = single_book.__name__
    """
    Get single book id

    Args:
        id (int):

    Returns:
        dict: book 
    """
    try:
        db = create_session()

        if id:
            get_single_book = get_single_book_id(db, id)

        elif authors:
            get_single_book = get_book_authors(db, authors)

        elif categories:
            get_single_book = get_book_categories(db, categories)

        elif title:
            get_single_book = get_book_title(db, title)

        if not get_single_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="email not exits"
            )
        return get_single_book
    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"error get users by email,{method}"
        )
    finally:
        db.close()


def create_book_library(form_in: LibraryRegistry) -> dict:
    method = create_book_library.__name__

    """
    create book in  database
    Body:
        form_in: is a LibraryRegistry model

    Returns:
        dict: book
    """
    try:
        db = create_session()

        return create_book(db, obj_in=form_in)

    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"error create form user, {method}"
        )
    finally:
        db.close()


def update_silgle_book(id: int, obj_updater: UpdateLibrary):
    method = update_silgle_book.__name__

    """
    Update a book record in the database
    """
    try:
        db = create_session()

        db_obj = single_book(id=id)
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NotItem)

        return update_book(db, obj_to_data=db_obj, obj_updater=obj_updater)
    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"error update user, {method}"
        )
    finally:
        db.close()


def delete_single_book(id: int):
    method = delete_single_book.__name__

    """
    Delete a single user record in the database

    """
    try:
        db = create_session()

        db_obj = single_book(id=id)
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NotItem)
        db_user = delete_book_title(db=db, id=id)
        return db_user
    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(
            status.HTTP_424_FAILED_DEPENDENCY, detail=f"error delete user, {method}"
        )
    finally:
        db.close()
