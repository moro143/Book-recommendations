import requests

def search_book(q):
    q = q.replace(" ", "+")
    link = "http://openlibrary.org/search.json?q=" + q
    print(link)
    response = requests.get(link)
    response = response.json()
    return response["docs"]
