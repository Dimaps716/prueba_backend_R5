import logging
from datetime import datetime

import requests
from fastapi import HTTPException, status

from repositories.library import create_book_for_consult


def convert_date(date_str):
    if date_str is None:
        return None
    date_format = "%Y" if len(date_str) == 4 else "%B %Y"
    try:
        return datetime.strptime(date_str, date_format).date()
    except ValueError:
        return None


def search_books_open_library(search_term, result):
    method = search_books_open_library.__name__
    try:

        url = f"https://openlibrary.org/search.json?q={search_term}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Procesar los resultados del API de Google Books
            books = data.get("docs", [])
            response_data = []
            for _ in range(10):
                book = books[_]
                response_data.append(
                    {
                        "title": book.get("title", ""),
                        "subtitle": book.get("subtitle", ""),
                        "authors": book.get("author_name", [])[0]
                        if book.get("author_name") is not None
                        else None,
                        "categories": book.get("categories", ""),
                        "editor": book.get("publisher", "")[0]
                        if book.get("publisher") is not None
                        else None,
                        "publication_date": convert_date(
                            str(book.get("first_publish_year", ""))
                        ),
                        "description": book.get("description", ""),
                        "image": book["imageLinks"].get("thumbnail", "")
                        if "imageLinks" in book
                        else "",
                    }
                )
            data = {"source": "Open Library API", "data": response_data}
            create_book_for_consult(response_data)

            result.put(data, block=True)

        else:
            result.put(response.status_code, block=True)

    except Exception as ex:
        logging.error(f"Error when execute {method}: {ex}")
        result.put({"Exception": ex})