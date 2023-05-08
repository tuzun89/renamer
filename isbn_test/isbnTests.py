import re
import pprint

# Define the ISBN regex pattern
# isbn_pattern = r"\bISBN(?:-1[03])?:?(?:\s+)?((?=(?:\d(?:[- ])?){9}[\dX])(?:\d(?:[- ])?){12}[\dX]|\d{9}[\dX])\b"

# isbn_pattern = r"\bISBN(?:-1[03])?:?(?:\s+)?((?=(?:\d(?:[- ])?){9}[\dX])(?:\d(?:[- ])?){12}[\dX]|\d{9}[\dX])\b" Result 17/24

isbn_pattern = r"(?:ISBN(?:-1[03])?:?\ )?(?P<isbn>(?:\d[\ |-]?){9,13}[\d|X])"


# Define the ISBN numbers to be tested
isbn_numbers = [

    # Valid ISBNs
    ("9781617292231", True),  # Valid ISBN13
    ("ISBN 978-1-78995-154-7", True),  # Valid ISBN13 with 'ISBN' prefix and hyphens
    ("ISBN-13: 978-0-13-235088-4", True),  # Valid ISBN13 with 'ISBN-13:' prefix and hyphens
    ("978-0596809485", True),  # Valid ISBN13 with hyphens
    ("1506715338", True),  # Valid ISBN10
    ("ISBN 1506715338", True),  # Valid ISBN10 with 'ISBN' prefix
    ("ISBN-10: 1506715338", True),  # Valid ISBN10 with 'ISBN-10:' prefix
    ("ISBN 978-1-61021-123-2", True),  # Valid ISBN13 with 'ISBN' prefix, hyphens and equals sign
    ("ISBN-13: 978-1-61021-123-2", True),  # Valid ISBN13 with 'ISBN-13:' prefix, hyphens and equals sign
    ("978-1-61021-123-2=", True),  # Valid ISBN13 with hyphens and equals sign
    ("978-0-13-235088-4", True),  # Valid ISBN13 with hyphens
    ("9780596809485", True),  # Valid ISBN13 without hyphens
    ("978 0 13 235088 4", True),  # Valid ISBN13 with spaces

    # Invalid ISBNs
    ("1234-567-89-0", False),  # Invalid ISBN with incorrect hyphen placement
    ("123456789", False),  # Invalid ISBN with less than 10 digits
    ("12345678901", False),  # Invalid ISBN with more than 13 digits
    ("978-0-13-235088-3", False),  # Invalid ISBN with incorrect checksum
    ("9781617292232", False),  # Invalid ISBN with incorrect checksum
    ("978161729223", False),  # Invalid ISBN with less than 13 digits
    ("978-1-61021-123-3", False),  # Invalid ISBN with incorrect checksum
    ("0123456789", False),  # Invalid ISBN with incorrect checksum
    ("01234567890", False),  # Invalid ISBN with more than 10 digits
    ("012345678", False),  # Invalid ISBN with less than 10 digits
    ("12 13 15 16 17", False),  # Invalid ISBN with spaces"
]

# Test the ISBN regex pattern against the ISBN numbers
failed_tests = []
passed_tests = 0
for i, (isbn, expected_result) in enumerate(isbn_numbers):
    try:
        assert bool(re.match(isbn_pattern, isbn)) == expected_result, isbn
        passed_tests += 1
        print(f"ISBN test {i+1} passed: {isbn} => {expected_result}")
    except AssertionError:
        failed_tests.append(isbn)
        print(f"\nISBN test {i+1} FAILED: {isbn} => {expected_result}\n")

# Print the results of the tests
if not failed_tests:
    print("All tests passed!")
    
print(f"\nValid ISBN Tests passed: {passed_tests}/{len(isbn_numbers)}")

"""
for i in isbn_numbers:
    print(i)
"""