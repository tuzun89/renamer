import re
import pprint

# Define the ISBN regex pattern
# isbn_pattern = r"\bISBN(?:-1[03])?:?(?:\s+)?((?=(?:\d(?:[- ])?){9}[\dX])(?:\d(?:[- ])?){12}[\dX]|\d{9}[\dX])\b"

# isbn_pattern = r"\bISBN(?:-1[03])?:?(?:\s+)?((?=(?:\d(?:[- ])?){9}[\dX])(?:\d(?:[- ])?){12}[\dX]|\d{9}[\dX])\b" Result 17/24

isbn_pattern = re.compile(r"(?P<isbn>\b(?:ISBN(?:-1[03])?:?\x20)?(?=.{17}$|.{13}$)[0-9]{1,5}(?:[- ]?[0-9]+){2}[- ]?[0-9X]\b)")

# Define the ISBN numbers to be tested
isbn_numbers = [
    # Valid ISBNs
    ("9781788395151", True),
    ("0-13-235088-2", True), # ISBN-10: 
    ("978-1-80107-356-1", True),
    ("978-1-83921-227-7", True), # ISBN-13: 
    ("978-1-78913-450-6", True), # ISBN 
    ("978-1-59749-957-6", True), # ISBN: 

    # Invalid ISBNs
    ("978-1-83882-779", False), # No check digit
    ("15 14 13 12", False), # Not ISBN format
    ("97818388277", False), # Not enough digits
    ("978-1-882-779-X", False), # Invalid hyphen placement and digit count
    ("978-1-83882-779", False), # Invalid in general
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