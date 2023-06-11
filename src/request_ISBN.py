import requests
import json

from pprint import pprint


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

    def get_modify_path_isbn_dict(
        self, final_modified_isbn: list[str]
    ) -> dict[str:str]:
        """
        modifies path_isbn_dict to contain only valid ISBNs
        """
        modified_path_isbn_dict = {}
        for key, value in self.path_isbn_dict.items():
            value = value.replace("-", "").replace(" ", "").replace("ISBN", "")

            if value in final_modified_isbn:
                modified_path_isbn_dict.update({key: value})

        return modified_path_isbn_dict

    def combine_dict(self, modified_path_isbn_dict: dict[str:str] = None):
        """
        filters out ISBNs that are not found in Google API and returns 2no dicts
        with contents in accordance with the results of request_book_by_ISBN() method

        returns filtered_dict(for OpenLib API) and included_dict(for GoogleBooks API)
        """
        included_dict = {}
        # If modified_path_isbn_dict is empty, then use the original path_isbn_dict
        if modified_path_isbn_dict is None:
            filtered_dict = self.path_isbn_dict.copy()
        else:
            filtered_dict = modified_path_isbn_dict.copy()

        keys_to_delete = []
        for key, value in filtered_dict.items():
            if value not in self.fallback_isbn:
                keys_to_delete.append(key)
                included_dict.update({key: value})
            else:
                pass

        # Delete keys from filtered_dict that are in keys_to_delete list outside of the main loop
        for key in keys_to_delete:
            del filtered_dict[key]

        # to-do: create a debug mode where helper print statements are shown
        # as per the below if statements
        if filtered_dict:
            pass
            # print(f"Filtered dictionary: {filtered_dict}\n")
        if included_dict:
            pass
            # pprint(f"Included dictionary: {included_dict}\n", width=120)
            # print(f"Included dictionary length: {len(included_dict)}\n")
        if self.fallback_isbn:
            pass
            # print(f"Fallback ISBN: {self.fallback_isbn}")
        if self.invalid_isbn:
            pass
            # print(f"Invalid ISBN: {self.invalid_isbn}\n")

        return filtered_dict, included_dict

    def remove_dashes(self, isbn):
        """
        not necessary as Google API can handle dashes in ISBN

        removes dashes and spaces from ISBNs
        """
        modified_isbns = []
        for i in isbn:
            str(
                modified_isbns.append(
                    i.replace("-", "").replace(" ", "").replace("ISBN", "")
                )
            )
        return modified_isbns

    def request_book_by_ISBN(self, modified_isbns):
        """
        make sure that you are not connected via VPN or proxy
        as Google API will not work (this may be WSL2 specific)

        iterates over the list of ISBNs and requests book data from Google API
        if no data is found, the ISBN is checked with the OpenLib API
        finally if the ISBN is invalid its added to a list of invalid ISBNs

        returns two lists of JSON objects (one for Google API and one for OpenLib API)
        """
        json_list = []
        json_list_openlib = []
        url_list = []
        final_modifieid_isbns = []

        for isbn in modified_isbns:
            # Google API URL does not require "ISBN" prefix
            url = "https://www.googleapis.com/books/v1/volumes?q=" + isbn
            try:
                response = requests.get(url)
                response.raise_for_status() # Raise an exception if the response status code is not 200
            except json.decoder.JSONDecodeError as e:
                self.invalid_isbn.append(isbn)
                # Delete the invalid ISBN from the dictionary, last added key:value pair
                # self.path_isbn_dict.popitem()
                # Delete the invalid ISBN from the modified_isbn list
                modified_isbns.remove(isbn)
                final_modifieid_isbns = modified_isbns
                print(
                    f"\nError: {e} indicates invalid ISBN: {self.invalid_isbn}, skipping...\n"
                )
                continue
            except Exception as e:
                self.invalid_isbn.append(isbn)
                # Delete the invalid ISBN from the dictionary
                # self.path_isbn_dict.popitem()
                # Delete the invalid ISBN from the modified_isbn list
                modified_isbns.remove(isbn)
                final_modifieid_isbns = modified_isbns
                print(f"\nError: {e} indicates invalid ISBN: {self.invalid_isbn}\n")
                continue
            data = response.json()
            # print(data)
            if data.get("totalItems") == 0:
                data = {}
                try:
                    url = "https://openlibrary.org/isbn/" + isbn + ".json"
                    response = requests.get(url)
                    response.raise_for_status() # Raise an exception if the response status code is not 200
                    data_open = response.json()
                    json_list_openlib.append(data_open)
                    self.fallback_isbn.append(isbn)

                except Exception as e:
                    self.invalid_isbn.append(isbn)
                    # Delete the invalid ISBN from the dictionary, last added key:value pair
                    # self.path_isbn_dict.popitem()
                    # Delete the invalid ISBN from the modified_isbn list
                    modified_isbns.remove(isbn)
                    final_modifieid_isbns = modified_isbns
                    print(
                        f"\nError: {e} indicates invalid ISBN: {self.invalid_isbn}, skipping...\n"
                    )
                    continue
                    # print(data)
            url_list.append(url)
            json_list.append(data)

        # print(f"JSON list length: {len(json_list)}")
        # print(f"URL list: {url_list}")
        # print(f"URL list length: {len(url_list)}")
        
        # These all return 1 less item than the number of ISBNs found.

        return json_list, json_list_openlib, final_modifieid_isbns

    def sort_json(self, json_list):
        """
        sorts JSON objects and returns a list of book names and authors
        for books that are found in Google API

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
