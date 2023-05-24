import os
from requestISBN import sortJson


class Renamer:
    def __init__(self) -> None:
        self.books_dict = {}

    def rename(self, books_dict):
        count = 0
        for old_path, new_name in books_dict.items():
            if os.path.exists(old_path):
                new_path = os.path.join(os.path.dirname(old_path), new_name)
                os.rename(old_path, new_path)
                count += 1
                print("Renamed", old_path, "to", new_path)
                self.books_dict.update({old_path: new_path})
            else:
                print("File not found:", old_path)
        print("\nNumber of renamed pdfs: ", count, "\n")
