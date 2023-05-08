import sys
import argparse
from extractor import Extractor
from renamer import Renamer
import requestISBN
from pprint import pprint


def args():
    parser = argparse.ArgumentParser(
        description="Rename ebook files as 'Author - Title - ISBN'"
    )
    parser.add_argument("path", metavar="path", help="filepath required")
    args = parser.parse_args()
    return args


def main(args):
    extractor = Extractor()
    renamer = Renamer()
    isbn_list = extractor.extractISBNs(args.path)
    print("\nNumber of ISBNs found:", len(isbn_list), "\n")
    pprint(isbn_list)
    print()
    isbns = requestISBN.splitDict(isbn_list)
    print(isbns)
    modified = requestISBN.removeDashes(isbns)
    print("Modified ISBN:", modified)
    json = requestISBN.requestISBN(modified)
    # pprint(json)
    req = requestISBN.sortJson(json, isbn_list)
    renamer.rename(req)


if __name__ == "__main__":
    main(args())
