import requests


class RequestISBN:
    def __init__(self, path_isbn_dict):
        self.path_isbn_dict = path_isbn_dict
        self.invalid_isbn = []
        self.fallback_isbn = []

    def split_dict(self):
        """
        obtain dict from extractor class and split key value pair to two lists
        """
        file = []
        isbn = []
        for key, value in self.path_isbn_dict.items():
            file.append(key)
            isbn.append(value)
        # print(file)
        # print(isbn)
        return isbn

    def combine_dict(self):
        """
        filters out ISBNs that are not found in Google API and returns 2no dicts
        with contents in accordance with the results of request_book_by_ISBN() method

        returns filtered_dict(for OpenLib API) and included_dict(for GoogleBooks API)
        """
        included_dict = {}
        filtered_dict = self.path_isbn_dict.copy()
        for key, value in self.path_isbn_dict.items():
            if value not in self.fallback_isbn:
                del filtered_dict[key]
                included_dict.update({key: value})
            else:
                pass
        # to-do: create a debug mode where helper print statements are shown
        # as per the below if statements
        if filtered_dict:
            pass
            # print(f"Filtered dictionary: {filtered_dict}\n")
        if included_dict:
            pass
            # print(f"Included dictionary: {included_dict}\n")
        if self.fallback_isbn:
            pass
            # print(f"Fallback ISBN: {self.fallback_isbn}")
        return filtered_dict, included_dict

    def remove_dashes(self, isbn):
        """
        not necessary as Google API can handle dashes in ISBN

        removes dashes and spaces from ISBNs
        """
        modified_isbn = []
        for i in isbn:
            str(
                modified_isbn.append(
                    i.replace("-", "").replace(" ", "").replace("ISBN", "")
                )
            )
        return modified_isbn

    def request_book_by_ISBN(self, modified_isbn):
        """
        make sure that you are not connected via VPN or proxy
        as Google API will not work (this may be WSL2 specific)

        iterates over the list of ISBNs and requests book data from Google API
        if no data is found, the ISBN is checked with the OpenLib API
        finally if the ISBN is invalied added to a list of invalid ISBNs (global)

        returns two lists of JSON objects (one for Google API and one for OpenLib API)
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
                    self.fallback_isbn.append(isbn)
                except Exception as e:
                    # global invalid_isbn
                    self.invalid_isbn.append(isbn)
                    print(f"Invalid ISBN: {self.invalid_isbn}")
                    raise e
                    # print(data)
            url_list.append(url)
            json_list.append(data)

        # print(json_list)
        # print(url_list)
        return json_list, json_list_openlib

    def sort_json(self, json_list):
        """
        sorts JSON objects and returns a list of book names and authors
        of books that are found in Google API

        returns a list of file (book) names of the form "author_title.pdf"

        todo: add support for multiple authors
        """
        books_list = []

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

    def sort_json_dict(self, books_list, included_dict):
        """
        uses the above generated books_list and returns a dictionary with key value pair of
        old path and new name of books that are found in Google API

        returns a dictionary with key value pair of old path and new name
        """
        google_books_dict = {}

        for key, value in included_dict.items():
            try:
                if books_list:
                    google_books_dict.update({key: books_list[0]})
                    books_list.pop(0)
                # else:
                #    failed_reqs.append(key)
            except Exception as e:
                print(f"Dictionary item creation error: {e} {key: value}\n")

        # print(books)
        # print(books_dict)
        return google_books_dict

    def sort_openlib(self, json_list_openlib):
        """
        sorts json from openlibrary.org as a fallback if Google API fails

        returns 2no lists of book names and authors
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

    def name_builder(self, titles, fixed_names):
        """
        builds a list of book names from the sorted lists of titles and authors

        returns a list of file (book) names of the form "authors_title.pdf"
        """
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

    def new_dict_builder(self, book_names, filtered_dict):
        """
        builds a dictionary with key value pair of old path and new book names

        returns dictionary with key value pair of old path and new book name
        """
        books_dict = {}

        for key, value in filtered_dict.items():
            try:
                if book_names:
                    books_dict.update({key: book_names[0]})
                    book_names.pop(0)

            except Exception as e:
                print("Dictionary item creation error:", e, {key: value}, "\n")

        return books_dict

    """
    if __name__ == "__main__":
        # rem = removeDashes(["978-1449340377"])
        req = request_book_by_ISBN(["9781449340377"])
        title, fixed_names = sort_openlib(req[1])
        book_names = name_builder(title, fixed_names)
        dicter = new_dict_builder(book_names, {"/path/to/book1":"978-1-80107-356-1","/path/to/book2":"978-1-78913-450-6","/path/to/book3":"9781449340377"})
        print(dicter)
    """
