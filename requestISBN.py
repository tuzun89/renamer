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


def requestISBN(isbn):
    json_list = []
    url_list = []
    for i in isbn:
        url = 'https://www.googleapis.com/books/v1/volumes?q=' + i + ".json"
        response = requests.get(url)
        json_list.append(response.json())
        url_list.append(url)
    return json_list


def sortJson(json_list):
    for i in json_list:
        if i['title']:
            print(i['title'])
        if i['authors']:
            print(i['authors'][0]['name'])
        else:
            print("No info found")
