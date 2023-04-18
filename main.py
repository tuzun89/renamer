import sys
import argparse
from extractor import Extractor
from pprint import pprint


def args():
    parser = argparse.ArgumentParser(
        description="Rename ebook files as 'Author - Title - ISBN'")
    parser.add_argument('path', metavar='path', help="filepath required")
    args = parser.parse_args()
    return args


def main(args):
    extractor = Extractor()
    isbn_list = extractor.extractISBNs(args.path)
    print("\nNumber of ISBNs found:", len(isbn_list), "\n")
    pprint(isbn_list)


if __name__ == '__main__':
    main(args())
