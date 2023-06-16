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
            return search_books(search_term)
    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"error {method}")

    finally:
        db.close()


def search_books(search_term):
    method = get_books_db.__name__
    try:
        result_queue = queue.Queue()

        search_functions = [
            google_books.search_books_in_google_api,
            books_open_library.search_books_open_library,
            books_library_of_congress.search_books_library_of_congress
        ]

        threads = [
            threading.Thread(
                target=search_function,
                args=(search_term, result_queue),
                daemon=True
            )
            for search_function in search_functions
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join(timeout=0.2)

        value_data = []
        while not result_queue.empty():
            value_data.append(result_queue.get_nowait())

        return value_data

    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"error {method}")



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
        get_single_book = ""

        if id:
            get_single_book = get_single_book_id(db, id)

        elif authors:
            get_single_book = get_book_authors(db, authors.rstrip())

        elif categories:
            get_single_book = get_book_categories(db, categories.rstrip())

        elif title:
            get_single_book = get_book_title(db, title.rstrip())

        if not get_single_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=method
            )
        return get_single_book
    except Exception as ex:
        logging.error(f"{method}: {ex}")
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"{method}"
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
            status.HTTP_404_NOT_FOUND, detail={method}
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
            status.HTTP_404_NOT_FOUND, detail=method
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
            status.HTTP_424_FAILED_DEPENDENCY, detail=f"error delete, {method}"
        )
    finally:
        db.close()
