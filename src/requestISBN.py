import requests
import re

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
        str(modified_isbn.append(i.replace("-", "").replace(" ", "").replace("ISBN", "")))
    return modified_isbn


"""
make sure that you are not connected via VPN or proxy as Google API will not work
"""


def requestISBN(modified_isbn):
    json_list = []
    url_list = []
    invalid_isbn = []
    for i in modified_isbn:
        url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + i
        response = requests.get(url)
        data = response.json()
        json_list.append(data)
        if data.get("totalItems") == 0:
            invalid_isbn.append(i)
            print("Invalid ISBN:", invalid_isbn)
        url_list.append(url)
    # print(json_list)
    # print(url_list)
    return json_list


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
            else:
                print("Required information not found")

    except Exception as e:
        print("\nJSON parsing error:", e, i, "\n")
        failed_reqs.append(i)
        print("Failed requests:", failed_reqs, "\n")

    
    for key, value in isbn_list.items():
        try:
            books_dict.update({key: books[0]})
            books.pop(0)
        except Exception as e:
            print("Dictionary item creation error:", e, {key:value}, "\n")
            continue

    #print(books)
    #print(books_dict)
    return books_dict
