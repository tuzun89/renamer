from find_isbn import FindISBN
import os

class Extractor:
    def __init__(self) -> None:
        self.path_isbn_dict = {}

    def extract_ISBNs(self, path):
        """
        Extracts ISBNs from all PDF files in a directory and its subdirectories.
        Returns a dictionary with the path as key and the ISBN as value.
        Profiling indicates that this function takes 89% of the total runtime,
        So tqdm progress bar is useful here.

        to-do: split into two functions for multithreading
        """
        for root, dirs, files in os.walk(path):
            # remove "no_isbns_found" directory from dirs
            if "no_isbns_found" in dirs:
                dirs.remove("no_isbns_found")
            # number_of_files = len(files)
            # print(f"Number of files found: {number_of_files}")
            for file_name in files:
                if file_name.endswith(".pdf"):
                    file_path = os.path.join(root, file_name)
                    find = FindISBN()
                    find.analyse_pdf(file_path)
                    isbn = find.get_isbn()

                    if isbn:
                        self.path_isbn_dict.update({file_path: isbn})

                elif os.path.isdir(file_path):
                    self.extract_ISBNs(file_path)

        return self.path_isbn_dict  # number_of_files

    # def extract_files
    # return list of all paths in original path (including subdirectories)
