import re
import os
import shutil

import PyPDF2

# PyPDF2 is no longer maintained. Use pypdf instead.
# to-do: replace PyPDF2 with pypdf --> https://pypi.org/project/pypdf/

from pdfminer.high_level import extract_text as fallback_extract_text


class FindISBN:
    def __init__(self) -> None:
        self.isbn = None
        self.not_isbn = None
        # ISBN number maybe of 2no formats (-13 or -10) and
        # the number might not be called up as ISBN on any given page
        # Regex below to match these conditions to find a number that matches the ISBN formats.
        # Regex does not match non-text ISBNs.
        self.isbn_pattern = re.compile(
            r"(?P<isbn>((?:(?<=ISBN[013: ]))?(97[89])-?(\d{1,5})-?(\d{1,7})-?(\d{1,6})-([\dXx{1}])|(0-\d{2}-?\d{5,}-?[\dXx{1}])|(978)[0-1+]\d{9}))"
        )

    def analyse_pdf(self, path):
        try:
            with open(path, "rb") as pdf_file:
                # print(f"Processing: {path}")
                pdf_reader = PyPDF2.PdfReader(pdf_file)
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
                    
                if not match:
                    self.not_isbn = path
                    print("\nNo ISBN found in", path)
                    self.file_mover()

            # When working files and using "with open" the file is closed automatically.
            # pdf_file.close() --> not needed

        except Exception as e:
            # PyPDF2._utils no longer exists.
            # https://pypdf.readthedocs.io/en/latest/user/suppress-warnings.html?highlight=error
            print(f"\nError reading PDF file: {path}")
            raise e

    def get_isbn(self):
        """
        returns filepath if ISBN number is found
        """
        return self.isbn

    def get_not_isbn(self):
        """
        returns filepath if ISBN number is NOT found
        """
        return self.not_isbn

    def validate_isbn(self, isbn):
        """
        checks if ISBN is valid
        to-do: implement ISBN validation
        """
        pass

    def file_mover(self):
        """
        moves files where no ISBN found to a new directory
        under parent directory called "no_isbns_found"
        """
        not_isbn = self.get_not_isbn()
        # print(not_isbn)

        if not_isbn and os.path.exists(not_isbn):
            file_path = os.path.abspath(not_isbn)
            # print(file_path)
            file_name = os.path.basename(file_path)
            # print(file_name)
            file_dir = os.path.dirname(file_path)
            # print(file_dir)
            new_dir = os.path.join(file_dir, "no_isbns_found")
            # print(new_dir)

            if os.path.exists(new_dir):
                print(f"Directory {new_dir} already exists")
            else:
                try:
                    os.mkdir(new_dir)
                except OSError as e:
                    print(f"Error creating directory: {new_dir}")
                    raise e

            new_path = os.path.join(new_dir, file_name)
            print(f"Moving file {file_name} to directory {new_path}")
            # shutil.move() moves a file or directory (src) to another location (dst)
            # high-level operation on files and collections of files
            # no need for low level os operations where new file names are created
            shutil.move(file_path, new_path)
