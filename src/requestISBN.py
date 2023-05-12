import requests
import re

invalid_isbn = []

"""
obtain dict from extractor class and split key value pair to two lists
"""


def splitDict(dict):
    file = []
    isbn = []
    for key, value in dict.items():
        file.append(key)
        isbn.append(value)
    # print(file)
    # print(isbn)
    return isbn


""""
not necessary as Google API can handle dashes in ISBN
"""


def removeDashes(isbn):
    print("ISBN:", isbn)
    modified_isbn = []
    for i in isbn:
        str(
            modified_isbn.append(
                i.replace("-", "").replace(" ", "").replace("ISBN", "")
            )
        )
    #print(modified_isbn)
    return modified_isbn


"""
make sure that you are not connected via VPN or proxy as Google API will not work
"""


def requestISBN(modified_isbn):
    json_list = []
    json_list_openlib = []
    url_list = []
    
    for i in modified_isbn:
        url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + i
        response = requests.get(url)
        data = response.json()
        json_list.append(data)
        if data.get("totalItems") == 0:
            try:
                url = "https://openlibrary.org/isbn/" + i + ".json"
                response = requests.get(url)
                data = response.json()
                json_list_openlib.append(data)
                # print(json_list_openlib)
            except Exception as e:
                invalid_isbn.append(i)
                # print("Invalid ISBN:", invalid_isbn)
        url_list.append(url)
    # print(json_list)
    # print(url_list)
    return json_list, json_list_openlib


def sortJson(json_list, isbn_list):
    books = []
    books_dict = {}
    failed_reqs = []

    try:
        for i in json_list:
            volumeInfo = i["items"][0]["volumeInfo"]
            if "items" in i and volumeInfo and "title" and "author":
                author = volumeInfo["authors"][0]
                parts = author.split()
                # print(parts)
                if len(parts) > 1:
                    surname = parts[-1]
                    initials = "".join([p[0] + "." for p in parts[:-1]])
                    author_name = surname + ", " + initials
                else:
                    author_name = author

                book_name = author_name + "_" + volumeInfo["title"] + ".pdf"
                # book_name = re.sub(r'[^A-Za-z0-9]+', '_', book_name)
                books.append(book_name)
                # print(books)
            
    except Exception as e:
        failed_reqs.append(i)

    for key, value in isbn_list.items():
        try:
            if books:
                books_dict.update({key: books[0]})
                books.pop(0)
            else:
                failed_reqs.append(key)
        except Exception as e:
            print("Dictionary item creation error:", e, {key: value}, "\n")
            failed_reqs.append(value)

    if failed_reqs:
        print("Failed requests for invalid ISBN: ", invalid_isbn, "returns ", failed_reqs, "\n")

    # print(books)
    # print(books_dict)
    return books_dict



"""
sorts json from openlibrary.org as a fallback if Google API fails
returns dictionary with key value pair of old path and new path
"""
def sort_openlib(json_list_openlib):

    try:

        title = []
        author_urls = []
        author_json_list = []
        fixed_names = []

        for i in json_list_openlib:
            title.append(i["title"])
            author_urls.append(i["authors"][0]["key"])
            author_urls.append(i["authors"][1]["key"])

            for i in author_urls:
                full_url = "https://openlibrary.org/" + i + ".json"
                response = requests.get(full_url)
                data = response.json()
                author_json_list.append(data)

            names = []
            
            for i in author_json_list:
                name = i["name"]
                names.append(i["name"])
                parts = name.split()
                if len(parts) > 1:
                    surname = parts[-1]
                    initials = "".join([p[0] + "." for p in parts[:-1]])
                    author_name = surname + ", " + initials
                    fixed_names.append(author_name)
                else:
                    author_name = name

    except Exception as e:
        print("Error:", e)
    
    print(title, fixed_names)
    return title, fixed_names

def name_builder(titles, fixed_names):

    book_names = []

    if len(titles) > 1:
        for title, author in zip(titles, fixed_names):
            authors = " & ".join(author)
            book_names.append(f"{authors}_{title}.pdf")
            return book_names
    else:
        authors = " & ".join(fixed_names)
        book_names.append(f"{authors}_{titles[0]}.pdf")
        print(book_names)
        return book_names

    
if __name__ == "__main__":
    # rem = removeDashes(["978-1449340377"])
    req = requestISBN(['9781449340377'])
    title, fixed_names = sort_openlib(req[1])
    name_builder(title, fixed_names)