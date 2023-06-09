import re
import os
import shutil
import threading

import PyPDF2
from PyPDF2.errors import PdfReadError


# PyPDF2 is no longer maintained. Use pypdf instead.
# to-do: replace PyPDF2 with pypdf --> https://pypi.org/project/pypdf/

from pdfminer.high_level import extract_text as fallback_extract_text


class FindISBN:
    def __init__(self) -> None:
        self.isbn: str = None
        self.not_isbn: list[str] = []
        self.move_count: int = 0
        # ISBN number maybe of 2no formats (-13 or -10) and
        # the number might not be called up as ISBN on any given page
        # Regex below to match these conditions to find a number that matches the ISBN formats.
        # Regex does not match non-text ISBNs.
        self.isbn_pattern: str = re.compile(
            r"(?P<isbn>((?:(?<=ISBN[013: ]))?(97[89])-?(\d{1,5})-?(\d{1,7})-?(\d{1,6})-([\dXx{1}])|(0-\d{2}-?\d{5,}-?[\dXx{1}])|(978)[0-1+]\d{9}))"
        )
        self.lock = threading.Lock()

    def analyse_pdf(self, path):
        """
        extracts ISBN from PDF file using regex if PyPDF2 fails, uses fallback method
        if ISBN found send value to isbn variable sends file to file_mover() if no ISBN found
        """
        # with self.lock:
        try:
            with self.lock, open(path, "rb") as pdf_file:
                # print(f"Processing: {path}")
                pdf_reader = PyPDF2.PdfReader(pdf_file, strict=False)
                # Limit the number of pages to read, first 30 and last 10
                if len(pdf_reader.pages) > 30:
                    initial_pages = range(0, 30)
                    final_pages = range(
                        len(pdf_reader.pages) - 10, len(pdf_reader.pages)
                    )
                    pages_to_read = list(initial_pages) + list(final_pages)
                else:
                    pages_to_read = range(0, len(pdf_reader.pages))
                for page_num in pages_to_read:
                    page = pdf_reader.pages[page_num]
                    try:
                        text = page.extract_text()
                    except Exception as e:
                        # try another PDF library
                        # this check all pages in the PDF
                        print(
                            f"{e} --> Trying fallback method to extract text from PDF: {path}"
                        )
                        text = fallback_extract_text(pdf_file)

                    match = self.isbn_pattern.search(text)

                    if match:
                        isbn = match.group("isbn")
                        self.validate_isbn(isbn)
                        self.isbn = isbn
                        break
                else:
                    # self.move_counter()
                    self.not_isbn.append(path)
                    # print("\nNo ISBN found in", self.not_isbn)
                    # self.file_mover(path)

            # When working files and using "with open" the file is closed automatically.
            # pdf_file.close() --> not needed

        except PdfReadError as e:
            # PyPDF2._utils no longer exists.
            # https://pypdf.readthedocs.io/en/latest/user/suppress-warnings.html?highlight=error
            print(f"\nError {e} reading PDF file: {path}")

    def move_counter(self):
        """
        returns number of files moved
        """
        with self.lock:
            self.move_count += 1
            print(f"Number of files moved: {self.move_count}")
            return self.move_count

    def get_isbn(self):
        """
        returns filepath if ISBN number is found
        """
        with self.lock:
            return self.isbn

    def get_not_isbn(self):
        """
        returns list of filepaths where ISBN number is NOT found
        """
        with self.lock:
            return self.not_isbn

    def validate_isbn(self, isbn: str) -> bool:
        """
        checks if ISBN is valid
        to-do: implement ISBN validation
        """
        pass

    def file_mover(self, not_isbn):
        """
        moves files where no ISBN found to a new directory
        under parent directory called "no_isbns_found"

        to-do: keep track of number of files moved
        """
        # not_isbn = self.get_not_isbn()
        with self.lock:

            for path in not_isbn:

                if not_isbn and os.path.exists(path):

                    file_path = os.path.abspath(path)
                    file_name = os.path.basename(file_path)
                    file_dir = os.path.dirname(file_path)
                    new_dir = os.path.join(file_dir, "no_isbns_found")

                    if not os.path.exists(new_dir):
                        # print(f"Directory {new_dir} already exists")
                        try:
                            os.mkdir(new_dir)
                        except OSError as e:
                            print(f"Error creating directory: {new_dir}")
                            raise e

                    new_path = os.path.join(new_dir, file_name)
                    # print(f"Moving file {file_name} to directory {new_path}")
                    # shutil.move() moves a file or directory (src) to another location (dst)
                    # high-level operation on files and collections of files
                    # no need for low level os operations where new file names are created
                    # print(f"File {file_name} moved to {new_path}")
                    shutil.move(file_path, new_path)

            return self.move_counter()
