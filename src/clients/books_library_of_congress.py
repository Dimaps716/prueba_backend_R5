from datetime import datetime

import requests

from repositories.library import create_book_for_consult


def convert_date(date_str):
    if date_str is None:
        return None
    date_format = "%Y" if len(date_str) == 4 else "%B %Y"
    try:
        return datetime.strptime(date_str, date_format).date()
    except ValueError:
        return None

def search_books_library_of_congress(search_term, result):
    url = f"https://www.loc.gov/books/?q={search_term}&fo=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        books = data.get("results", [])
        response_data = []
        for _ in range(10):
            book = books[_]
            response_data.append(
                {
                    "title": book.get("item", "")["title"],
                    "subtitle": book.get("subtitle", ""),
                    "authors": book.get("item", "")["contributors"][0],
                    "categories": book.get("partof", [])[0],
                    "editor": book.get("group", "")[0],
                    "publication_date": convert_date(str(book.get("date", ""))),
                    "description": book.get("description", "")[0] if book.get("description") is not None else None,
                    "image": book.get("image_url", "")[0],
                }
            )
        data = {"source": "Library of Congress API", "data": response_data}
        create_book_for_consult(response_data)

        result.put(data, block=True)
    else:
        result.put(response.status_code, block=True)
