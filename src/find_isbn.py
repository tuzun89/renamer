import PyPDF2
import re


class FindISBN:
    def __init__(self) -> None:
        self.isbn = None
        self.not_isbn = None

    def analyse_pdf(self, path):
        try:
            # resources_dict = {}
            with open(path, "rb") as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    # ISBN number maybe of 2no formats (-13 or -10) and
                    # the number might not be called up as ISBN on any given page
                    # Regex below to match these conditions to find a number that matches the ISBN formats.
                    # Regex does not match non-text ISBNs.
                    isbn_pattern = re.compile(
                        r"(?P<isbn>((?:(?<=ISBN[013: ]))?(97[89])-?(\d{1,5})-?(\d{1,7})-?(\d{1,6})-([\dXx{1}])|(0-\d{2}-?\d{5,}-?[\dXx{1}])|(978)[0-1+]\d{9}))"
                    )

                    match = isbn_pattern.search(text)

                    if match:
                        isbn = match.group("isbn")
                        self.validate_isbn(isbn)
                        self.isbn = isbn
                        print(f"Processing: {path}")
                        break

                if not match:
                    self.not_isbn = path
                    print("\nNo ISBN found in", path)

                pdf_file.close()

        except PyPDF2._utils.PdfStreamError:
            print("\nError reading PDF file:", path)

    def get_isbn(self):
        return self.isbn

    def get_not_isbn(self):
        return self.not_isbn

    def validate_isbn(self, isbn):
        """
        checks if ISBN is valid
        """
        pass
