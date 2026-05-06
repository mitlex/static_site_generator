import unittest

from gencontent import *

class TestGenContent(unittest.TestCase):

    #-------------extract_title Tests-------------

    def test_extract_title(self):
        md = """# This is an h1 header when converted to html"""
        self.assertEqual(
            extract_title(md), 
            """This is an h1 header when converted to html"""
        )

    def test_extract_title_strip_whitespace(self):
        md = """#     This is an h1 header when converted to html    """
        self.assertEqual(
            extract_title(md), 
            """This is an h1 header when converted to html"""
        )

    def test_extract_title_two_titles(self):
        md = """# This is an h1 header when converted to html
# This is a second h1 header but we'll return the first h1 header"""
        self.assertEqual(
            extract_title(md), 
            """This is an h1 header when converted to html"""
        )

    def test_extract_title_numerous_lines(self):
        md = """This is a test

### for multiple lines of markdown before a header appears

# This is an h1 header when converted to html"""
        self.assertEqual(
            extract_title(md), 
            """This is an h1 header when converted to html"""
        )

    def test_extract_title_wrong_header_type(self):
        md = """### This is an h3 header when converted to html"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_no_h1(self):
        md = """This md does not contain an h1 header"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_no_h1_but_hash_in_text(self):
        md = """This md does not # contain an h1 header"""
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()