import sys
from extractor import Extractor
from pprint import pprint

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python file.py path")
        sys.exit(1)
    path = sys.argv[1]
    
extractor = Extractor()
isbn_list = extractor.extractISBNs()

print("\nNumber of ISBNs found:", len(isbn_list), "\n")

pprint(isbn_list)
    