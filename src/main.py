import sys
import os
import argparse
from extractor import Extractor
from renamer import Renamer
import requestISBN
from pprint import pprint


class Main:
    def __init__(self):
        self.extractor = Extractor()
        self.renamer = Renamer()

    def args(self):
        parser = argparse.ArgumentParser(
            description="Rename ebook files as 'Author - Title - ISBN'"
        )
        parser.add_argument("path", metavar="path", help="filepath required")
        args = parser.parse_args()
        return args

    def openlib_isbn(self):
        filtered_dict, included_dict = requestISBN.combine_dict(self.path_isbn_dict)

        print(
            f"Number of ISBNs found in the OpenLibrary API: {len(self.json_list_openlib[:])} \n"
        )

        title, fixed_names = requestISBN.sort_openlib(self.json_list_openlib)
        print("Sorted OpenLibrary data:", title, fixed_names)
        book_names = requestISBN.name_builder(title, fixed_names)
        print("Generated book names:", book_names)
        new_books_dict = requestISBN.new_dict_builder(book_names, filtered_dict)
        print("Generated new dictionary:", new_books_dict)
        # self.renamer.rename(new_dict)

        return new_books_dict
        """
        for old_path, new_name in new_dict.items():
            print("Processing:", old_path)
            if os.path.exists(old_path):
                self.renamer.rename({old_path: new_name})
            else:
                print("File not found:", old_path)
        """

    def main(self, args):
        # path_isbn_dict, number_of_files = self.extractor.extractISBNs(args.path)
        path_isbn_dict = self.extractor.extractISBNs(args.path)
        self.path_isbn_dict = path_isbn_dict  # store path_isbn_dict as an attribute
        # print(f"\nNumber of ISBNs found: {(len(path_isbn_dict))}/{number_of_files}\n")
        # pprint(path_isbn_dict)
        print()
        isbns = requestISBN.splitDict(path_isbn_dict)
        # print(isbns)
        modified = requestISBN.removeDashes(isbns)
        # print(f"Modified ISBN: {modified} \n")
        json_list, json_list_openlib = requestISBN.requestISBN(modified)
        # pprint(json_openlib)
        # pprint(json)
        books_list = requestISBN.sortJson(json_list)
        filtered_dict, included_dict = requestISBN.combine_dict(self.path_isbn_dict)
        google_books_dict = requestISBN.sort_json_dict(books_list, included_dict)
        print(google_books_dict)

        if len(google_books_dict) >= 1:
            self.renamer.rename(google_books_dict)

        if type(json_list_openlib) == list and len(json_list_openlib) >= 1:
            try:
                self.json_list_openlib = json_list_openlib
                new_books_dict = self.openlib_isbn()
                if new_books_dict is not None:
                    self.renamer.rename(new_books_dict)
                    self.json_list_openlib = []

            except SystemError as e:
                print("There is a problem with the OpenLibrary API", e)

        else:
            print(
                f"All {len(path_isbn_dict)} ISBNs were found in the Google Books API\n"
            )


"""
def main(args):
    path_isbn_dict, number_of_files = extractor.extractISBNs(args.path)
    print(f"\nNumber of ISBNs found: {(len(path_isbn_dict))}/{number_of_files}\n")
    pprint(path_isbn_dict)
    print()
    isbns = requestISBN.splitDict(path_isbn_dict)
    # print(isbns)
    modified = requestISBN.removeDashes(isbns)
    print(f"Modified ISBN: {modified} \n")
    json, json_openlib = requestISBN.requestISBN(modified)
    # pprint(json_openlib)
    # pprint(json)
    google_books_dict = requestISBN.sortJson(json)
    books_dict = requestISBN.sort_json_dict(google_books_dict, path_isbn_dict)
    # print(books_dict)

    if len(books_dict) >= 1:
        renamer.rename(books_dict)

    if type(json_openlib) == list and len(json_openlib) >= 1:
        try:
            openlib_isbn()

        except SystemError as e:
            print("There is a problem with the OpenLibrary API", e)

    else:
        print(f"All {len(path_isbn_dict)} ISBNs were found in the Google Books API\n")
"""


if __name__ == "__main__":
    Main().main(Main().args())
