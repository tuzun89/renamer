from find_isbn import FindISBN
from pprint import pprint
import os

class Extractor:
    def __init__(self) -> None:
        self.folder = 'test'
        #self.isbn_list = []
        self.dict = {}

    def extractISBNs(self):
        for root, dirs, files in os.walk(self.folder):
            for file_name in files:
                if file_name.endswith('.pdf'):
                    file_path = os.path.join(root, file_name)
                    #print(file_path)
                    find = FindISBN()
                    find.analyse_pdf(file_path)
                    isbn = find.get_isbn()

                    if isbn:
                        #self.isbn_list.append(isbn)
                        self.dict.update({file_path:isbn})

            pprint(self.dict)
        return self.dict
    
    # each time an isbn is found, add it to a dictionary with the file path as the key
    # return the dictionary at the end of the function

    
    
