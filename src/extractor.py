from find_isbn import FindISBN
import os


class Extractor:
    def __init__(self) -> None:
        self.dict = {}

    def extractISBNs(self, path):
        for root, dirs, files in os.walk(path):
            # number_of_files = len(files)
            # print(f"Number of files found: {number_of_files}")
            for file_name in files:
                if file_name.endswith(".pdf"):
                    file_path = os.path.join(root, file_name)
                    find = FindISBN()
                    find.analyse_pdf(file_path)
                    isbn = find.get_isbn()

                    # print(f"Processing: {file_path}")

                    if isbn:
                        self.dict.update({file_path: isbn})

                elif os.path.isdir(file_path):
                    self.extractISBNs(file_path)

        return self.dict  # number_of_files
