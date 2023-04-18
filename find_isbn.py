import PyPDF2
import re


class FindISBN:
    def __init__(self) -> None:
        self.isbn = None
        self.not_isbn = None

    def analyse_pdf(self, path):
        with open(path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                # ISBN number maybe of 2no formats (-13 or -10) and 
                # the number might not be called up as ISBN on any given page
                # Regex below to match these conditions to find a number that matches the ISBN formats.
                isbn_pattern = re.compile(
                    r"(?P<isbn>\d{3}-\d{1,5}-\d{1,7}-\d{1,6}-\d)")
                match = isbn_pattern.search(text)

                if match:
                    isbn = match.group('isbn')
                    self.isbn = isbn
                    break

            if not match:
                self.not_isbn = path
                print("\nNo ISBN found in", path)

            pdf_file.close()

    def get_isbn(self):
        return self.isbn

    def get_not_isbn(self):
        return self.not_isbn