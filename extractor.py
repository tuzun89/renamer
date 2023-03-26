from renamer import Renamer
import os

class Extractor:
    def __init__(self) -> None:
        self.folder = 'test'
        self.isbn_list = []

    def extractor(self):
        for root, dirs, files in os.walk(self.folder):
            for file_name in files:
                if file_name.endswith('.pdf'):
                    file_path = os.path.join(root, file_name)

                    renamer = Renamer()
                    renamer.analyse_pdf(file_path)
                    isbn = renamer.get_isbn()

                    if isbn:
                        self.isbn_list.append(isbn)
        
        return self.isbn_list