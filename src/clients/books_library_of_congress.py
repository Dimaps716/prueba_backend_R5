import requests


def search_books_library_of_congress(search_term, result):
    url = f"https://www.loc.gov/books/?q={search_term}&fo=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        books = data.get("results", [])
        response_data = []
        for book in books:
            response_data.append(
                {
                    "title": book.get("item", "")["title"],
                    "subtitle": book.get("subtitle", ""),
                    "authors": book.get("item", "")["contributors"],
                    "categories": book.get("partof", []),
                    "editor": book.get("group", ""),
                    "publication_date": book.get("dates", ""),
                    "description": book.get("description", ""),
                    "image": book.get("image_url", ""),
                }
            )
        data = {"source": "Library of Congress API", "data": response_data}

        result.put(data, block=True)
    else:
        result.put(response.status_code, block=True)
