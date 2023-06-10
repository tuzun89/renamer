import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import (
    Manager,
)  # Import the Manager object from the multiprocessing module as lock can't be pickled in threading

# import threading

from find_isbn import FindISBN

from tqdm import tqdm


class Extractor:
    def __init__(self) -> None:
        self.path_isbn_dict = {}
        self.not_isbn_file_path = []
        self.lock = Manager().Lock()

    def extract_ISBNs(self, original_path: str) -> dict[str, str]:
        """
        Extracts ISBNs from list of pathnames.

        Returns a dictionary with the path as key and the ISBN as value.

        Profiling indicates that this function takes 89% of the total runtime,
        So tqdm progress bar is useful here.
        """
        pathnames = self.collect_pathnames(original_path)
        stack = [original_path]
        while stack:
            path = stack.pop()
            try:
                with ProcessPoolExecutor() as executor:
                    results = list(
                        tqdm(
                            executor.map(self.process_pdf_files, pathnames),
                            total=len(pathnames),
                            desc="Extracting ISBNs",
                        )
                    )

                    # print(type(results))
                    # print(results)

                for result in results:
                    if result is not None:
                        path, isbn = result  # unpack tuple
                        if isbn is not None:
                            self.path_isbn_dict[path] = isbn  # add to dictionary

                return self.path_isbn_dict  # number_of_files

            finally:
                executor.shutdown(wait=True)

    def collect_pathnames(self, path: str) -> list[str]:
        """
        Walks the original path arguement passed in to create a list of pathnames (incl. All sub-dirs)
        """
        pathnames = []
        print(f"\nProcessing files in directory --> {path}")
        for root, dirs, files in os.walk(path):
            # Make a copy of the dirs before modifying it
            dirs_copy = dirs.copy()
            # remove "no_isbns_found" directory from dirs
            if "no_isbns_found" in dirs_copy:
                dirs_copy.remove("no_isbns_found")
            # number_of_files = len(files)
            # print(f"Number of files found: {number_of_files}")
            for file_name in files:
                if file_name.endswith(".pdf"):
                    file_path = os.path.join(root, file_name)
                    pathnames.append(file_path)
            # Recursively call function to walk through sub-directories
            for file_path in dirs_copy:
                if os.path.isdir(file_path):
                    self.extract_ISBNs(file_path)

        # print(f"Pathnames collected: {len(pathnames)}")
        # print(f"Pathnames: {pathnames}")

        return pathnames

    def process_pdf_files(self, file_path):
        """
        process a single pdf file

        returns a dictionary with the path as key and the ISBN as value
        """
        # thread_id = threading.get_ident()
        # print(f"Thread ID: {thread_id} processing file: {file_path}")
        with self.lock:
            find = FindISBN()
            find.analyse_pdf(file_path)
            isbn = find.get_isbn()
            not_isbn = find.get_not_isbn()

            if isbn:
                return file_path, isbn
            else:
                print(f"Where ISBN is not found: {not_isbn}")
                self.not_isbn_file_path.append(file_path)
                print(f"Shape of not_isbn list: {self.not_isbn_file_path}")

    def get_not_isbn_file_path(self) -> list[str]:
        """
        returns string representation of filepaths where ISBN number is NOT found
        """
        while True:
            not_isbn_file_path = self.not_isbn_file_path.copy()
            if not not_isbn_file_path:
                break
            print(f"Files where ISBN number is NOT found: {not_isbn_file_path}")
            time.sleep(1)
        return not_isbn_file_path
