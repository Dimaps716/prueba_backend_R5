from datetime import datetime

import requests

from repositories.library import create_book, create_book_for_consult


def convert_date(date_str):
    if date_str is None:
        return None
    if len(date_str) == 4:  # Si la cadena tiene solo el año
        return datetime.strptime(date_str, "%Y").date()
    else:  # Si la cadena tiene el año, mes y día
        return datetime.strptime(date_str, "%Y-%m-%d").date()


def search_books_in_google_api(search_term: str, result) -> list:
    url = f"https://www.googleapis.com/books/v1/volumes?q={search_term}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Procesar los resultados del API de Google Books
        books = data.get("items", [])

        response_data = []
        for book in books:
            book_info = book.get("volumeInfo", {})

            response_data.append(
                {
                    "title": book_info.get("title", ""),
                    "subtitle": book_info.get("subtitle", ""),
                    "authors": book_info.get("authors", "")[0]
                    if type(book_info.get("authors")) is list
                    else book_info.get("authors", ""),
                    "categories": book_info.get("categories", "")[0]
                    if type(book_info.get("categories")) is list
                    else book_info.get("categories", ""),
                    "editor": book_info.get("publisher", ""),
                    "publication_date": convert_date(
                        book_info.get("publishedDate", "")
                    ),
                    "description": book_info.get("description", ""),
                    "image": book_info["imageLinks"].get("thumbnail", "")
                    if "imageLinks" in book_info
                    else "",
                }
            )

            data = {"source": "Google Books", "data": response_data}
        create_book_for_consult(response_data)
        result.put(data, block=True)
    else:
        result.put(response.status_code, block=True)
