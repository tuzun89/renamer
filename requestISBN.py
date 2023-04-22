import requests
from extractor import Extractor

"""
define function to obtain dict from extractor class and split key value pair to two lists
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


def removeDashes(isbn):
    modified_isbn = []
    for i in isbn:
        modified_isbn.append(i.replace("-", ""))
    return modified_isbn


def requestISBN(modified_isbn):
    json_list = []
    url_list = []
    for i in modified_isbn:
        url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + i
        response = requests.get(url)
        json_list.append(response.json())
        url_list.append(url)
    # print(json_list)
    # print(url_list)
    return json_list


def sortJson(json_list):
    for i in json_list:
        volumeInfo = i['items'][0]['volumeInfo']
        if 'items' in i and volumeInfo and 'title' and 'author':
            author = volumeInfo['authors'][0]
            parts = author.split()
            # print(parts)
            if len(parts) > 1:
                surname = parts[-1]
                initials = ''.join([p[0] + '.' for p in parts[:-1]])
                author_name = surname + ', ' + initials
            else:
                author_name = author
            book_name = (author_name + "_" + volumeInfo['title'])
            print(book_name)
        else:
            print("Required information not found")
    print()
    return book_name
