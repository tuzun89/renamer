import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from find_isbn import FindISBN

from tqdm import tqdm


class Extractor:
    def __init__(self) -> None:
        self.path_isbn_dict = {}
        self.not_isbn_file_path = []
        self.lock = threading.Lock()

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
                # Make a copy of the dirs before modyfying it
                dirs_copy = dirs.copy()
                # remove "no_isbns_found" directory from dirs
                if "no_isbns_found" in dirs_copy:
                    dirs_copy.remove("no_isbns_found")
                # number_of_files = len(files)
                # print(f"Number of files found: {number_of_files}")
                for file_name in files:
                    if file_name.endswith(".pdf"):
                        file_path = os.path.join(root, file_name)
                        futures.append(
                            executor.submit(self.process_pdf_files, file_path)
                        )
                for file_path in dirs_copy:
                    if os.path.isdir(file_path):
                        futures.append(executor.submit(self.extract_ISBNs, file_path))
            with tqdm(total=len(futures), desc="Extracting ISBNs") as pbar:
                for future in as_completed(futures):
                    result = future.result()
                    if result is not None:
                        file_path, isbn = result  # unpack tuple
                        self.path_isbn_dict[file_path] = isbn  # add to dictionary
                    pbar.update(1)
                    pbar.set_description(f"ISBN extracted from: {file_path}")
            # wait for all threads to finish and then shutdown
            executor.shutdown(wait=True)

        return self.path_isbn_dict  # number_of_files

    def process_pdf_files(self, file_path):
        """
        process a single pdf file

        returns a dictionary with the path as key and the ISBN as value
        """
        thread_id = threading.get_ident()
        # print(f"Thread ID: {thread_id} processing file: {file_path}")
        find = FindISBN()
        find.analyse_pdf(file_path)
        isbn = find.get_isbn()
        not_isbn = find.get_not_isbn()

        if isbn:
            return file_path, isbn
        elif not_isbn:
            self.not_isbn_file_path.append(file_path)

    def not_isbn_file_path(self) -> list[str]:
        """
        returns string representation of filepaths where ISBN number is NOT found
        """
        return self.not_isbn_file_path