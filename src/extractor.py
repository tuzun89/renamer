import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from find_isbn import FindISBN


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
        print(f"\nProcessing files in directory --> {path}")
        with ThreadPoolExecutor() as executor:
            futures = []
            for root, dirs, files in os.walk(path):
                # remove "no_isbns_found" directory from dirs
                if "no_isbns_found" in dirs:
                    dirs.remove("no_isbns_found")
                # number_of_files = len(files)
                # print(f"Number of files found: {number_of_files}")
                for file_name in files:
                    if file_name.endswith(".pdf"):
                        file_path = os.path.join(root, file_name)
                        futures.append(
                            executor.submit(self.process_pdf_files, file_path)
                        )
                for file_path in dirs:
                    if os.path.isdir(file_path):
                        futures.append(executor.submit(self.extract_ISBNs, file_path))
            for future in as_completed(futures):
                result = future.result()
                if result is not None:
                    file_path, isbn = result  # unpack tuple
                    self.path_isbn_dict[file_path] = isbn   # add to dictionary

        return self.path_isbn_dict  # number_of_files

    def process_pdf_files(self, file_path):
        """
        process a single pdf file

        returns a dictionary with the path as key and the ISBN as value
        """
        thread_id = threading.get_ident()
        print(f"Thread ID: {thread_id} processing file: {file_path}")
        find = FindISBN()
        find.analyse_pdf(file_path)
        isbn = find.get_isbn()

        if isbn:
            return file_path, isbn
        else:
            return None
