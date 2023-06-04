from datetime import datetime

import requests

from repositories.library import create_book, create_book_for_consult


def convert_date(date_str):
    if date_str is None:
        return None
    if isinstance(date_str, int):  # If the input is a 4-digit year as an integer
        date_str = str(date_str)
    date_format = "%Y-%m-%d" if len(date_str) > 7 else "%Y-%m"
    try:
        return datetime.strptime(date_str, date_format).date()
    except ValueError:
        return None


def search_books_in_google_api(search_term: str, result) -> list:
    url = f"https://www.googleapis.com/books/v1/volumes?q={search_term}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Procesar los resultados del API de Google Books
        books = data.get("items", [])

        response_data = []
        for _ in range(10):
            book = books[_].get("volumeInfo", {})

            response_data.append(
                {
                    "title": book.get("title", ""),
                    "subtitle": book.get("subtitle", ""),
                    "authors": book.get("authors", "")[0]
                    if type(book.get("authors")) is list
                    else book.get("authors", ""),
                    "categories": book.get("categories", "")[0]
                    if type(book.get("categories")) is list
                    else book.get("categories", ""),
                    "editor": book.get("publisher", ""),
                    "publication_date": convert_date(
                        book.get("publishedDate", "")
                    ),
                    "description": book.get("description", ""),
                    "image": book["imageLinks"].get("thumbnail", "")
                    if "imageLinks" in book
                    else "",
                }
            )

            data = {"source": "Google Books", "data": response_data}
        create_book_for_consult(response_data)
        result.put(data, block=True)
    else:
        result.put(response.status_code, block=True)
