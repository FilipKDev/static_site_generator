import unittest
from block_markdown import markdown_to_blocks, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):
    def test_one_line(self):
        document = "This document has one line"
        expected_output = ["This document has one line"]
        self.assertEqual(markdown_to_blocks(document), expected_output)

    def test_two_line_block(self):
        document = """\
* First item on the list
* Second item on the list"""
        expected_output = [
            "* First item on the list\n* Second item on the list"
        ]
        self.assertEqual(markdown_to_blocks(document), expected_output)

    def test_heading_and_paragraph(self):
        document = """\
# Document heading

A paragraph of text."""
        expected_output = [
            "# Document heading",
            "A paragraph of text."
        ]
        self.assertEqual(markdown_to_blocks(document), expected_output)

    def test_heading_paragraph_list(self):
        document = """\
# This is a heading

And this is a paragraph of text after the heading. It has words in it.

* This is the start of a list
* Second list item
* Third list item"""
        expected_output = [
            "# This is a heading",
            "And this is a paragraph of text after the heading. It has words in it.",
            "* This is the start of a list\n* Second list item\n* Third list item"
        ]
        self.assertEqual(markdown_to_blocks(document), expected_output)

    def test_white_space(self):
        document = """\
# This is a heading with some trailing white space     

        And this is a paragraph of text with leading white space. It has words in it.

* This is the start of a list
     * Second list item with leading and trailing whitespace   
* Third list item"""
        expected_output = [
            "# This is a heading with some trailing white space",
            "And this is a paragraph of text with leading white space. It has words in it.",
            "* This is the start of a list\n* Second list item with leading and trailing whitespace\n* Third list item"
        ]
        self.assertEqual(markdown_to_blocks(document), expected_output)

    def test_excessive_newlines(self):
        document = """\
# This is a heading and a lot of newlines









And a paragraph at the end."""
        expected_output = [
            "# This is a heading and a lot of newlines",
            "And a paragraph at the end."
        ]
        self.assertEqual(markdown_to_blocks(document), expected_output)

    def test_white_space_excessive_newlines(self):
        document = """\
# This is a heading with some trailing white space     






      And this is a paragraph of text with leading white space. It has words in it.

* This is the start of a list




   * Second list item with leading and trailing whitespace   
* Third list item





"""
        expected_output = [
            "# This is a heading with some trailing white space",
            "And this is a paragraph of text with leading white space. It has words in it.",
            "* This is the start of a list",
            "* Second list item with leading and trailing whitespace\n* Third list item"
        ]
        self.assertEqual(markdown_to_blocks(document), expected_output)

class TestBlockToBlockType(unittest.TestCase):
    def test_normal(self):
        document = """\
This is a normal paragraph without any special characters.
"""
        self.assertEqual(block_to_block_type(document), "normal")

    def test_heading(self):
        document = """\
### HEADING
"""
        self.assertEqual(block_to_block_type(document), "heading")

    def test_invalid_heading(self):
        document = """\
####### HEADING WITH TOO MANY HASH CHARACTERS
"""
        self.assertNotEqual(block_to_block_type(document), "heading")

    def test_code(self):
        document = """\
```A code block
With some extra lines```
"""
        self.assertEqual(block_to_block_type(document), "code")

    def test_quote(self):
        document = """\
> Quote 1
> Quote 2
> Quote 3
"""
        self.assertEqual(block_to_block_type(document), "quote")

    def test_unordered_list(self):
        document = """\
* List Item 1
* List Item 2
* List Item 3
"""
        self.assertEqual(block_to_block_type(document), "unordered list")

    def test_ordered_list(self):
        document = """\
1. Ordered List Item 1
2. Ordered List Item 2
3. Ordered List Item 3
4. Ordered List Item 4
"""
        self.assertEqual(block_to_block_type(document), "ordered list")

    def test_mistake(self):
        document = """\
1. Ordered List Item 1
* Oops a mistake
## another mistake
"""
        self.assertEqual(block_to_block_type(document), "normal")

if __name__ == "__main__":
    unittest.main()