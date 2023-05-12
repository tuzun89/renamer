import os
from requestISBN import sortJson

class Renamer:
    def __init__(self) -> None:
        self.books_dict = {}

    def rename(self, books_dict):
        for old_path, new_name in books_dict.items():
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            os.rename(old_path, new_path)
            print("Renamed", old_path, "to", new_path)
            self.books_dict.update({old_path: new_path})
        print("\nNumber of renamed pdfs: ", len(self.books_dict), "\n")
