import requests
import re

invalid_isbn = []
fallback_isbn = []


def splitDict(dict):
    """
    obtain dict from extractor class and split key value pair to two lists
    """
    file = []
    isbn = []
    for key, value in dict.items():
        file.append(key)
        isbn.append(value)
    # print(file)
    # print(isbn)
    return isbn


def combine_dict(dict):
    global fallback_isbn
    print(fallback_isbn)
    included_dict = {}
    filtered_dict = dict.copy()
    for key, value in dict.items():
        if value not in fallback_isbn:
            del filtered_dict[key]
            included_dict.update({key: value})
        else:
            pass
    print(filtered_dict)
    print(included_dict)
    return filtered_dict, included_dict


def removeDashes(isbn):
    """
    not necessary as Google API can handle dashes in ISBN
    """
    # print("ISBN:", isbn)
    modified_isbn = []
    for i in isbn:
        str(
            modified_isbn.append(
                i.replace("-", "").replace(" ", "").replace("ISBN", "")
            )
        )
    # print(modified_isbn)
    return modified_isbn


def requestISBN(modified_isbn):
    """
    make sure that you are not connected via VPN or proxy as Google API will not work
    """
    json_list = []
    json_list_openlib = []
    url_list = []

    for isbn in modified_isbn:
        url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn
        response = requests.get(url)
        data = response.json()
        # print(data)
        if data.get("totalItems") == 0:
            data = {}
            try:
                url = "https://openlibrary.org/isbn/" + isbn + ".json"
                response = requests.get(url)
                data_open = response.json()
                json_list_openlib.append(data_open)
                fallback_isbn.append(isbn)
                # print(json_list_openlib)
            except Exception as e:
                # global invalid_isbn
                invalid_isbn.append(isbn)
                print("Invalid ISBN:", invalid_isbn)
                # print(data)
        url_list.append(url)
        json_list.append(data)

    # print(json_list)
    # print(url_list)
    return json_list, json_list_openlib


def sortJson(json_list):
    books_list = []
    # books_dict = {}
    # failed_reqs = []

    try:
        for i in json_list:
            if "items" in i:
                volumeInfo = i["items"][0]["volumeInfo"]
                if "title" in volumeInfo and "authors" in volumeInfo:
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
                    books_list.append(book_name)
                # print(books)

    except Exception as e:
        print(f"Error: {e}")

    return books_list


def sort_json_dict(books_list, included_dict):
    google_books_dict = {}

    for key, value in included_dict.items():
        try:
            if books_list:
                google_books_dict.update({key: books_list[0]})
                books_list.pop(0)
            # else:
            #    failed_reqs.append(key)
        except Exception as e:
            print("Dictionary item creation error:", e, {key: value}, "\n")

    # print(books)
    # print(books_dict)
    return google_books_dict


def sort_openlib(json_list_openlib):
    """
    sorts json from openlibrary.org as a fallback if Google API fails
    returns dictionary with key value pair of old path and new path
    """
    try:
        title = []
        author_urls = []
        author_json_list = []
        fixed_names = []
        path_isbn_dict = {}

        for i in json_list_openlib:
            title.append(i["title"])
            author_urls.append(i["authors"][0]["key"])
            author_urls.append(i["authors"][1]["key"])
            path_isbn_dict.update()

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

    # print(path_isbn_dict)
    return title, fixed_names


def name_builder(titles, fixed_names):
    book_names = []

    if len(titles) > 1:
        for title, author in zip(titles, fixed_names):
            authors = " & ".join(author)
            book_names.append(f"{authors}_{title}.pdf")

    else:
        authors = " & ".join(fixed_names)
        book_names.append(f"{authors}_{titles[0]}.pdf")
        # print(book_names)

    return book_names


def new_dict_builder(book_names, filtered_dict):
    books_dict = {}

    for key, value in filtered_dict.items():
        try:
            if book_names:
                books_dict.update({key: book_names[0]})
                book_names.pop(0)

        except Exception as e:
            print("Dictionary item creation error:", e, {key: value}, "\n")

    print(books_dict)

    return books_dict


"""
if __name__ == "__main__":
    # rem = removeDashes(["978-1449340377"])
    req = requestISBN(["9781449340377"])
    title, fixed_names = sort_openlib(req[1])
    book_names = name_builder(title, fixed_names)
    dicter = new_dict_builder(book_names, {"/path/to/book1":"978-1-80107-356-1","/path/to/book2":"978-1-78913-450-6","/path/to/book3":"9781449340377"})
"""
