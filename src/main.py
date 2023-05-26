import argparse

from extractor import Extractor
from renamer import Renamer
from request_ISBN import RequestISBN


class Main:
    def __init__(self):
        self.extractor = Extractor()
        self.renamer = Renamer()
        self.args = self.parse_args()
        self.path_isbn_dict = self.extractor.extract_ISBNs(self.args.path)
        self.isbn_request = RequestISBN(self.path_isbn_dict)

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

    def openlib_isbn(self):
        """
        additional method to rename files using OpenLibrary API
        depending on if statement checks in main()

        returns new_books_dict to be sent back to main()
        """
        filtered_dict, included_dict = self.isbn_request.combine_dict()

        print(
            f"Number of ISBNs found in the OpenLibrary API: {len(self.json_list_openlib[:])} \n"
        )

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
        modified = self.isbn_request.remove_dashes(isbns)
        # print(f"Modified ISBN: {modified} \n")
        json_list, json_list_openlib = self.isbn_request.request_book_by_ISBN(modified)
        # pprint(json_openlib)
        # pprint(json)
        books_list = self.isbn_request.sort_json(json_list)
        filtered_dict, included_dict = self.isbn_request.combine_dict()
        google_books_dict = self.isbn_request.sort_json_dict(books_list, included_dict)
        # print(google_books_dict)

        if len(google_books_dict) >= 1:
            # with tqdm(total=len(google_books_dict),desc="Google Books API renaming files") as pbar:
            self.renamer.rename(google_books_dict)  # pbar.update)

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

        else:
            print(
                f"\nAll {len(self.path_isbn_dict)} ISBNs were found in the Google Books API\n"
            )


if __name__ == "__main__":
    main = Main()
    args = main.parse_args()
    print(f"\nProcessing files in directory --> {args.path}\n")
    main.main(args)
    """
    cProfile.run("main.main(args)", "profile")
    stats = pstats.Stats("profile")
    stats.sort_stats("cumulative").print_stats()
    """
