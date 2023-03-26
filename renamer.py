import PyPDF2
import re

class Renamer:
    def __init__(self) -> None:
        self.isbn = None
        self.check_digit = None

    def analyse_pdf(self, path):
        with open(path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            print(len(pdf_reader.pages))

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                #print(text)
                # ISBN number maybe of 2no formats (-13 or -10) and the number might not be called up as ISBN on any given page
                # Regex below to match these conditions to find a number that matches the ISBN formats.
                isbn_pattern = re.compile(r"(?P<isbn>\d{3}-\d{1,5}-\d{1,7}-\d{1,6}-\d)")
                match = isbn_pattern.search(text)
                #print(match)
                
                if match:
                    isbn = match.group('isbn')
                    #check_digit = match.group('check')
                    self.isbn = isbn
                    break
                """    
                    if len(isbn) == 10 and check_digit:
                        check_sum = sum((i + 1) * int(digit) for i, digit in enumerate(isbn))
                        if self.check_digit.lower() == 'x':
                            expected_check_digit = '10'
                        else:
                             expected_check_digit = str(check_sum % 11)
                        if self.check_digit != expected_check_digit:
                            self.isbn = ''
                """
            pdf_file.close()

    def get_isbn(self):
        return self.isbn