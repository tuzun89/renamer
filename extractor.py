from find_isbn import FindISBN
from pprint import pprint
import os

class Extractor:
    def __init__(self) -> None:
        self.dict = {}

    def extractISBNs(self, path):
        for root, dirs, files in os.walk(path):
            for file_name in files:
                if file_name.endswith('.pdf'):
                    file_path = os.path.join(root, file_name)
                    find = FindISBN()
                    find.analyse_pdf(file_path)
                    isbn = find.get_isbn()

                    if isbn:
                        self.dict.update({file_path: isbn})

        return self.dict