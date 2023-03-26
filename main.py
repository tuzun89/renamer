import sys
from renamer import Renamer
from extractor import Extractor
from pprint import pprint

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python file.py path")
        sys.exit(1)
    path = sys.argv[1]
    
extractor = Extractor()
isbn_list = extractor.extractor()

pprint(len(isbn_list))
pprint(isbn_list)
    