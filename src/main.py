import argparse
import sys

from extractor import Extractor
from renamer import Renamer
from request_ISBN import RequestISBN
from find_isbn import FindISBN

from pprint import pprint


class Main:
    def __init__(self):
        self.find = FindISBN()
        self.extractor = Extractor()
        self.renamer = Renamer()
        self.args = self.parse_args()
        self.path_isbn_dict = self.extractor.extract_ISBNs(self.args.path)
        # self.not_isbn_file_path = self.extractor.not_isbn_file_path[:]

        # print(self.not_isbn_file_path)
        self.isbn_request = RequestISBN(self.path_isbn_dict)
        self.google_books_dict = {}
    
    def get_google_books_dict(self):
        # Access the google_books_dict attribute
        print(self.google_books_dict.keys())

    def parse_args(self):
        """
        generates command line arguments

        returns the args object to be sent to main()
        """
        parser = argparse.ArgumentParser(
            description="Rename ebook files as 'Author - Title - ISBN'"
        )
        parser.add_argument("path", metavar="path", help="filepath required")
        args = parser.parse_args()
        return args

    def print_fallback(self):
        """
        prints fallback ISBNs to console
        """
        print(
            f"{len(self.isbn_request.fallback_isbn)}no fallback ISBN(s) detected: {self.isbn_request.fallback_isbn} --> ",
            f"Number of ISBN(s) found in the OpenLibrary API: {len(self.json_list_openlib[:])}no \n",
        )

    def google_results_summary(self, google_books_dict):
        """
        prints output from google_books_dict to console
        """
        print(
            f"\nNumber of ISBN(s) found on Google Book API: {len(google_books_dict)}no"
        )

    def openlib_isbn(self):
        """
        additional method to rename files using OpenLibrary API
        depending on if statement checks in main()

        returns new_books_dict to be sent back to main()
        """
        filtered_dict, included_dict = self.isbn_request.combine_dict()

        self.print_fallback()

        title, fixed_names = self.isbn_request.sort_openlib(self.json_list_openlib)
        # print("Sorted OpenLibrary data:", title, fixed_names)
        book_names = self.isbn_request.name_builder(title, fixed_names)
        # print("Generated book names:", book_names)
        new_books_dict = self.isbn_request.new_dict_builder(book_names, filtered_dict)
        # print("Generated new dictionary:", new_books_dict)
        # self.renamer.rename(new_dict)

        return new_books_dict

    def main(self, args):
        """
        main method to run the program
        instantiates the Extractor, Renamer, and RequestISBN classes
        """
        # print(f"\nProcessing files in directory --> {args.path}\n")
        # path_isbn_dict, number_of_files = self.extractor.extractISBNs(args.path)
        # path_isbn_dict = self.extractor.extract_ISBNs(args.path)
        # self.path_isbn_dict = path_isbn_dict  # store path_isbn_dict as an attribute
        # print(f"\nNumber of ISBNs found: {(len(path_isbn_dict))}/{number_of_files}\n")
        # pprint(path_isbn_dict)
        isbns = self.isbn_request.split_dict()
        # print(isbns)
        modified_isbns = self.isbn_request.remove_dashes(isbns)
        # print(f"Modified ISBN: {modified} \n")
        (
            json_list,
            json_list_openlib,
            final_modified_isbns,
        ) = self.isbn_request.request_book_by_ISBN(modified_isbns)
        print(f"Final modified ISBNs: {final_modified_isbns}\n")
        print(f"Final modified ISBNs length: {len(final_modified_isbns)}\n")
        # pprint(json_openlib)
        # pprint(json)
        books_list = self.isbn_request.sort_json(json_list)
        pprint(f"Books list: {books_list}\n", width=120)
        print(f"Books list length: {len(books_list)}\n")

        if len(final_modified_isbns) >= 1:
            # Create a new dictionary without the invalid ISBNs
            self.modified_path_isbn_dict = self.isbn_request.get_modify_path_isbn_dict(
                final_modified_isbns
            )
            pprint(
                f"Modified path ISBN dictionary: {self.modified_path_isbn_dict}\n",
                width=120,
            )
            print(
                f"\nModified path ISBN dictionary length: {len(self.modified_path_isbn_dict)}\n"
            )
            # Pass new dictionary to combine_dict method
            filtered_dict, included_dict = self.isbn_request.combine_dict(
                self.modified_path_isbn_dict
            )
        else:
            # If there are no invalid ISBNs, pass original dictionary to combine_dict method
            filtered_dict, included_dict = self.isbn_request.combine_dict()

        print(
            f"State of 'self.modified_path_isbn_dict' before the sort_json_dict() call: {self.modified_path_isbn_dict.keys()}"
        )
        print(
            f"State of 'google_books_dict' before the sort_json_dict() call: {self.get_google_books_dict()}"
        )

        self.google_books_dict = self.isbn_request.sort_json_dict(books_list, included_dict)

        print(
            f"State of 'self.modified_path_isbn_dict' after the sort_json_dict() call: {self.modified_path_isbn_dict.keys()}"
        )
        print(
            f"State of 'google_books_dict' after the sort_json_dict() call: {self.get_google_books_dict()}"
        )

        if len(self.google_books_dict) >= 1:
            # with tqdm(total=len(google_books_dict),desc="Google Books API renaming files") as pbar:
            pprint(f"Google Books dictionary: {self.google_books_dict}\n", width=120)
            # self.renamer.rename(google_books_dict)  # pbar.update)
            self.google_results_summary(self.google_books_dict)

            missing_keys = set(self.modified_path_isbn_dict.keys()) - set(
                self.google_books_dict.keys()
            )

            for key in missing_keys:
                print(
                    f"\n{key} is missing with value {self.modified_path_isbn_dict[key]}"
                )

            # Compare the keys of the dictionaries
            if set(self.modified_path_isbn_dict.keys()) != set(
                self.google_books_dict.keys()
            ):
                print("The dictionaries have different keys")
            else:
                # Compare the values of the dictionaries
                for key in self.modified_path_isbn_dict:
                    if self.modified_path_isbn_dict[key] != self.google_books_dict[key]:
                        print(f"\nThe value for key {key} is different")

        if type(json_list_openlib) == list and len(json_list_openlib) >= 1:
            try:
                self.json_list_openlib = json_list_openlib
                new_books_dict = self.openlib_isbn()
                if new_books_dict is not None:
                    # with tqdm(total=len(new_books_dict),desc="Open Library API renaming files") as pbar:
                    self.renamer.rename(new_books_dict)  # , pbar.update)
                self.json_list_openlib = []

            except SystemError as e:
                print("There is a problem with the OpenLibrary API", e)


if __name__ == "__main__":
    main = Main()
    args = main.parse_args()
    main.main(args)
    """
    cProfile.run("main.main(args)", "profile")
    stats = pstats.Stats("profile")
    stats.sort_stats("cumulative").print_stats()
    """
