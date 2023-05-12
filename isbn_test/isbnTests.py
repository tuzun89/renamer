import re

# Define the ISBN regex pattern
# isbn_pattern = r"\bISBN(?:-1[03])?:?(?:\s+)?((?=(?:\d(?:[- ])?){9}[\dX])(?:\d(?:[- ])?){12}[\dX]|\d{9}[\dX])\b"
# isbn_pattern = re.compile(r"(?P<isbn>((\b97[89]-?\b)-[0-1+]-?-\d{5,}-?\d{3,}-?[\dXx{1}])|(0-\d{2}-?\d{5,}-?[\dXx{1}])|(978)[0-1+]\d{9})") # best one so far

isbn_pattern = re.compile(
    r"(?P<isbn>((?:(?<=ISBN[013: ]))?(97[89])-?(\d{1,5})-?(\d{1,7})-?(\d{1,6})-([\dXx{1}])|(0-\d{2}-?\d{5,}-?[\dXx{1}])|(978)[0-1+]\d{9}))"
)

# Define the ISBN numbers to be tested
isbn_numbers = [
    # Valid ISBNs
    ("9781788395151", True),
    ("0-13-235088-2", True),  # ISBN-10:
    ("978-1-80107-356-1", True),
    ("978-1-83921-227-7", True),  # ISBN-13:
    ("978-1-78913-450-6", True),  # ISBN
    ("978-1-59749-957-6", True),  # ISBN:
    ("978-1-59749-957-X", True),
    ("978-0-9847828-5-7", True),  # Cracking the coding interview
    ("671-3447ISBN-13: 978-0-13-235088-4", True),
    ("ISBN 978-1-83921-206-2", True),
    ("4ISBN-10:        0-13-235088-2Text printed", True),
    # Invalid ISBNs
    ("978-1-83882-779", False),  # No check digit
    ("15 14 13 12", False),  # Not ISBN format
    ("97818388277", False),  # Not enough digits
    (
        "978-1-882-779-X",
        False,
    ),  # Invalid digit count. This needs to be corrected via checksum. Regex does not check for this.
    ("97801360918172", False),  # Invalid in general
    (
        "9788401459978",
        False,
    ),  # Invalid ISBN number with correct start and correct check digits
]

test_string = "All rights reserved. Printed in the United States of America. This publication is protected by copyright,and permission must be obtained from the publisher prior to any prohibited reproduction, storage in a retrieval system, or transmission in any form or by any means, electronic, mechanical, photocopying, recording, or likewise. For information regarding permissions, write to:Pearson Education, IncRights and Contracts Department501 Boylston Street, Suite 900Boston, MA 02116Fax: (617) 671-3447ISBN-13: 978-0-13-235088-4ISBN-10:        0-13-235088-2Text printed in the United States on recycled paper at Courier in Stoughton, Massachusetts.First printing July, 2008www.it-ebooks.info"


def find_isbn(test_string):
    match = isbn_pattern.search(test_string)
    if match:
        print(f"Matched ISBN: {match.group('isbn')}")
        return match.group("isbn")
    else:
        return "\nNo ISBN found in text."


def find_isbn_list():
    # Test the ISBN regex pattern against the ISBN numbers
    failed_tests = []
    passed_tests = 0
    for i, (isbn, expected_result) in enumerate(isbn_numbers):
        match = re.fullmatch(isbn_pattern, isbn)
        try:
            assert bool(match) == expected_result, isbn
            passed_tests += 1
            print(f"ISBN test {i+1} passed: {isbn} => {expected_result}")
            if match:
                print(f"Matched ISBN: {match.group()}")
        except AssertionError:
            failed_tests.append(isbn)
            print(f"ISBN test {i+1} FAILED: {isbn} => {expected_result}")
            print(f"Matched ISBN: {match}")
    # Print the results of the tests
    if not failed_tests:
        print("All tests passed!")

    print(f"\nISBN Tests passed: {passed_tests}/{len(isbn_numbers)}")

    """
    for i in isbn_numbers:
        print(i)
    """


isbn_list = find_isbn_list()
isbn_text = find_isbn(test_string)
