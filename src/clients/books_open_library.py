import requests


def search_books_open_library(search_term, result):
    url = f"https://openlibrary.org/search.json?q={search_term}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Procesar los resultados del API de Google Books
        books = data.get("results", [])
        response_data = []
        for book in books:
            response_data.append(
                {
                    "title": book.get("title", ""),
                    "subtitle": book.get("subtitle", ""),
                    "authors": book.get("author_name", []),
                    "categories": book.get("categories", []),
                    "editor": book.get("publisher", ""),
                    "publication_date": book.get("publish_date", "")[0],
                    "description": book.get("description", ""),
                    "image": book["imageLinks"].get("thumbnail", "")
                    if "imageLinks" in book
                    else "",
                }
            )
        data = {"source": "Open Library API", "data": response_data}

        result.put(data, block=True)

    else:
        result.put(response.status_code, block=True)
