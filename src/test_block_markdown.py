import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import split_nodes_delimiter

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
            "* This is the start of a list\n     * Second list item with leading and trailing whitespace   \n* Third list item"
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




   * Second list item with leading whitespace 
* Third list item with trailing white space       





"""
        expected_output = [
            "# This is a heading with some trailing white space",
            "And this is a paragraph of text with leading white space. It has words in it.",
            "* This is the start of a list",
            "* Second list item with leading whitespace \n* Third list item with trailing white space"
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

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_no_blocks(self):
        markdown = """\
"""
        expected_output = HTMLNode("div", None, [])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_single_block_paragraph_no_inline_syntax(self):
        markdown = """\
Just some text without any special syntax.
"""
        expected_output = HTMLNode("div", None, 
        [
            ParentNode("p", [
                ParentNode("", [LeafNode(None, "Just some text without any special syntax.")])
            ])])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_single_block_heading_no_inline_syntax(self):
        markdown = """\
## HEADING WITH 2 HASHES
"""
        expected_output = HTMLNode("div", None, 
        [
            ParentNode("h2", [
                LeafNode(None, "HEADING WITH 2 HASHES")
        ])])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)
    
    def test_single_block_code_no_inline_syntax(self):
        markdown = """\
```
CODE LINE 1
CODE LINE 2
```
"""
        expected_output = HTMLNode("div", None, 
        [
            ParentNode("pre", [
                LeafNode("code", "CODE LINE 1<br>"),
                LeafNode("code", "CODE LINE 2")
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    
    def test_single_block_quote_no_inline_syntax(self):
        markdown = """\
> Quote Line 1
> Quote Line 2
> Quote Line 3
"""
        expected_output = HTMLNode("div", None,
        [
            ParentNode("blockquote", [
                LeafNode(None, "Quote Line 1"), 
                LeafNode(None, "Quote Line 2"), 
                LeafNode(None, "Quote Line 3")
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_single_block_unordered_list_no_inline_syntax(self):
        markdown = """\
* Unordered List Item 1
* Second list item
* Final item on the list
"""
        expected_output = HTMLNode("div", None, [
            ParentNode("ul", [
                ParentNode("li", [LeafNode(None, "Unordered List Item 1")]),
                ParentNode("li", [LeafNode(None, "Second list item")]),
                ParentNode("li", [LeafNode(None, "Final item on the list")])
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_single_block_ordered_list_no_inline_syntax(self):
        markdown = """\
1. First item on the ordered list
2. Item 2
3. Ordered list item 3
"""
        expected_output = HTMLNode("div", None, [
            ParentNode("ol", [
                ParentNode("li", [LeafNode(None, "First item on the ordered list")]), 
                ParentNode("li", [LeafNode(None, "Item 2")]), 
                ParentNode("li", [LeafNode(None, "Ordered list item 3")])
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)


    def test_single_block_syntax_mistake_no_exception_no_inline_syntax(self):
        markdown = """\
List item 1
2. List item 2
`Code`
Some code
`Code2`
"""
        expected_output = HTMLNode("div", None, [
            ParentNode("p", [
                ParentNode("", [LeafNode(None, "List item 1")]),
                ParentNode("", [LeafNode(None, "2. List item 2")]),
                ParentNode("", [LeafNode("code", "Code")]),
                ParentNode("", [LeafNode(None, "Some code")]),
                ParentNode("", [LeafNode("code", "Code2")])
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_single_block_invalid_inline_syntax_exception(self):
        markdown = """\
* List item 1
list item 2
"""
        with self.assertRaises(ValueError):
            markdown_to_html_node(markdown)

    def test_single_block_paragraph_inline_syntax(self):
        markdown = """\
Just some text with **bold words** and *italic words*.
"""
        expected_output = HTMLNode("div", None, 
        [
            ParentNode("p", [
                ParentNode("", [
                    LeafNode(None, "Just some text with "),
                    LeafNode("b", "bold words"),
                    LeafNode(None, " and "),
                    LeafNode("i", "italic words"),
                    LeafNode(None, ".")
                    ])
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_single_block_heading_inline_syntax(self):
        markdown = """\
#### **BOLD** HEADING
"""
        expected_output = HTMLNode("div", None, 
        [
            ParentNode("h4", [
                LeafNode("b", "BOLD"),
                LeafNode(None, " HEADING")
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_single_block_code_inline_syntax(self):
        markdown = """\
```
CODE **LINE** 1
CODE *LINE* 2
```
"""
        expected_output = HTMLNode("div", None, 
        [
            ParentNode("pre", [
                LeafNode("code", "CODE **LINE** 1<br>"),
                LeafNode("code", "CODE *LINE* 2")
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_single_block_quote_inline_syntax(self):
        markdown = """\
> Quote Line with **bold** words
> *Italic words* in quote line 2
> This `code` exists in this quote line
"""
        expected_output = HTMLNode("div", None,
        [
            ParentNode("blockquote", [
                LeafNode(None, "Quote Line with "), 
                LeafNode("b", "bold"), 
                LeafNode(None, " words"), 
                LeafNode("i", "Italic words"),
                LeafNode(None, " in quote line 2"),
                LeafNode(None, "This "),
                LeafNode("code", "code"),
                LeafNode(None, " exists in this quote line")
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_single_block_unordered_list_inline_syntax(self):
        markdown = """\
* Unordered **List Item** 1
* Second `list item`
* Final **item** on the *list*
"""
        expected_output = HTMLNode("div", None, [
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode(None, "Unordered "),
                    LeafNode("b", "List Item"),
                    LeafNode(None, " 1")
                    ]),
                ParentNode("li", [
                    LeafNode(None, "Second "),
                    LeafNode("code", "list item")
                    ]),
                ParentNode("li", [
                    LeafNode(None, "Final "),
                    LeafNode("b", "item"),
                    LeafNode(None, " on the "),
                    LeafNode("i", "list")
                    ])
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_single_block_ordered_list_inline_syntax(self):
        markdown = """\
1. First *item* on the ordered list
2. **Item 2**
3. `Ordered` list `item` 3
"""
        expected_output = HTMLNode("div", None, [
            ParentNode("ol", [
                ParentNode("li", [
                    LeafNode(None, "First "),
                    LeafNode("i", "item"),
                    LeafNode(None, " on the ordered list")
                    ]),
                ParentNode("li", [
                    LeafNode("b", "Item 2")
                    ]),
                ParentNode("li", [
                    LeafNode("code", "Ordered"),
                    LeafNode(None, " list "),
                    LeafNode("code", "item"),
                    LeafNode(None, " 3")
                    ])
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_single_block_syntax_mistake_no_exception_inline_syntax(self):
        markdown = """\
**Bold words** and *italic words*
2. List item 2
`Code` and words
Some `code`
`Code2`
"""
        expected_output = HTMLNode("div", None, [
            ParentNode("p", [
                ParentNode("", [
                    LeafNode("b", "Bold words"),
                    LeafNode(None, " and "),
                    LeafNode("i", "italic words")
                    ]),
                ParentNode("", [LeafNode(None, "2. List item 2")]),
                ParentNode("", [
                    LeafNode("code", "Code"),
                    LeafNode(None, " and words")
                    ]),
                ParentNode("", [
                    LeafNode(None, "Some "),
                    LeafNode("code", "code")
                    ]),
                ParentNode("", [LeafNode("code", "Code2")])
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_single_block_paragraph_links_and_images(self):
        markdown = """\
This is a paragraph with [a link to Google](https://www.google.co.uk/) and an ![image of a pixel](https://dummyimage.com/1x1.png)
"""
        expected_output = HTMLNode("div", None, [
            ParentNode("p", [
                ParentNode("", [
                    LeafNode(None, "This is a paragraph with "),
                    LeafNode("a", "a link to Google", {"href": "https://www.google.co.uk/"}),
                    LeafNode(None, " and an "),
                    LeafNode("img", "", {"src": "https://dummyimage.com/1x1.png", "alt": "image of a pixel"})
                    ])
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_single_block_unordered_list_links(self):
        markdown = """\
* [YouTube](https://www.youtube.com/)
* [Twitch](https://www.twitch.tv/)
* [Udemy](https://www.udemy.com/)
"""
        expected_output = HTMLNode("div", None, [
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode("a", "YouTube", {"href": "https://www.youtube.com/"})
                    ]),
                ParentNode("li", [
                    LeafNode("a", "Twitch", {"href": "https://www.twitch.tv/"})
                    ]),
                ParentNode("li", [
                    LeafNode("a", "Udemy", {"href": "https://www.udemy.com/"})
                    ])
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_single_block_ordered_list_images(self):
        markdown = """\
1. ![1 pixel](https://dummyimage.com/1x1.png)
2. ![4 pixels](https://dummyimage.com/2x2.png)
3. ![16 pixels](https://dummyimage.com/4x4.png)
"""
        expected_output = HTMLNode("div", None, [
            ParentNode("ol", [
                ParentNode("li", [
                    LeafNode("img", "", {"src": "https://dummyimage.com/1x1.png", "alt": "1 pixel"})
                    ]),
                ParentNode("li", [
                    LeafNode("img", "", {"src": "https://dummyimage.com/2x2.png", "alt": "4 pixels"})
                    ]),
                ParentNode("li", [
                    LeafNode("img", "", {"src": "https://dummyimage.com/4x4.png", "alt": "16 pixels"})
                    ])
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_three_blocks_heading_paragraph_unordered_list(self):
        markdown = """\
##### **BOLD HEADING**

This is a paragraph with `some code` in it.

- List Item 1
- Second item in an unordered list
- Item 3 with some *italic words*
"""
        expected_output = HTMLNode("div", None, [
            ParentNode("h5", [
                LeafNode("b", "BOLD HEADING")
            ]),
            ParentNode("p", [
                ParentNode("", [
                    LeafNode(None, "This is a paragraph with "),
                    LeafNode("code", "some code"),
                    LeafNode(None, " in it.")
                ])
            ]),
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode(None, "List Item 1")
                ]),
                ParentNode("li", [
                    LeafNode(None, "Second item in an unordered list")
                ]),
                ParentNode("li", [
                    LeafNode(None, "Item 3 with some "),
                    LeafNode("i", "italic words")
                ])
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_three_blocks_code_paragraph_ordered_list(self):
        markdown = """\
```
c = 'some code'
return c
```

Some **bold** and *italic* words.

1. List Item 1
2. List Item 2
3. List Item 3
"""
        expected_output = HTMLNode("div", None, [
            ParentNode("pre", [
                LeafNode("code", "c = 'some code'<br>"),
                LeafNode("code", "return c")
            ]),
            ParentNode("p", [
                ParentNode("", [
                    LeafNode(None, "Some "),
                    LeafNode("b", "bold"),
                    LeafNode(None, " and "),
                    LeafNode("i", "italic"),
                    LeafNode(None, " words.")
                    ])
            ]),
            ParentNode("ol", [
                ParentNode("li", [LeafNode(None, "List Item 1")]),
                ParentNode("li", [LeafNode(None, "List Item 2")]),
                ParentNode("li", [LeafNode(None, "List Item 3")])
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_three_blocks_quotes_quotes_paragraph(self):
        markdown = """\
> Quote Line 1
> Quote Line 2
> Quote Line 3

> More quotes 1
> More quotes 2

Final paragraph with [a link to Wikipedia](https://en.wikipedia.org/wiki/Main_Page)
"""
        expected_output = HTMLNode("div", None, [
            ParentNode("blockquote", [
                LeafNode(None, "Quote Line 1"),
                LeafNode(None, "Quote Line 2"),
                LeafNode(None, "Quote Line 3")
            ]),
            ParentNode("blockquote", [
                LeafNode(None, "More quotes 1"),
                LeafNode(None, "More quotes 2")
            ]),
            ParentNode("p", [
                ParentNode("", [
                    LeafNode(None, "Final paragraph with "),
                    LeafNode("a", "a link to Wikipedia", {"href": "https://en.wikipedia.org/wiki/Main_Page"})
                ])
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

    def test_full_markdown(self):
        markdown = """\
###### This is a full document written in markdown

It has various markdown types that are split into **blocks** by *this markdown function*.

For example, an unordered list:

* With `a code block` in this line
* Or a list item containing **some bold words**
* Or `all types` of **supported** *syntax*

> According to all known laws of aviation, 
> there is no way a bee should be able to fly. 
> Its wings are too small to...

Above is a quote block. 
And below is an ordered list with *images* and *links*.

1. This list item is ![an image of the Tarantula Nebula](https://stsci-opo.org/STScI-01GA76RM0C11W977JRHGJ5J26X.png)
2. And this is a link [to NASA website](https://www.nasa.gov/)
3. This `list item` has a *link* to [Wikipedia article about Hubble Space Telescope](https://en.wikipedia.org/wiki/Hubble_Space_Telescope) and an ![image of said telescope](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/HST-SM4.jpeg/800px-HST-SM4.jpeg)

Finally, there is a code block with an example of a `for` loop function in **Python**.

```
for i in range(0, 10)
    print(i)
```
"""
        expected_output = HTMLNode("div", None, [
            ParentNode("h6", [LeafNode(None, "This is a full document written in markdown")]),
            ParentNode("p", [
                ParentNode("", [
                    LeafNode(None, "It has various markdown types that are split into "),
                    LeafNode("b", "blocks"),
                    LeafNode(None, " by "),
                    LeafNode("i", "this markdown function"),
                    LeafNode(None, ".")
                ])
            ]),
            ParentNode("p", [
                ParentNode("", [LeafNode(None, "For example, an unordered list:")])
            ]),
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode(None, "With "),
                    LeafNode("code", "a code block"),
                    LeafNode(None, " in this line")
                ]),
                ParentNode("li", [
                    LeafNode(None, "Or a list item containing "),
                    LeafNode("b", "some bold words")
                ]),
                ParentNode("li", [
                    LeafNode(None, "Or "),
                    LeafNode("code", "all types"),
                    LeafNode(None, " of "),
                    LeafNode("b", "supported"),
                    LeafNode(None, " "),
                    LeafNode("i", "syntax")
                ])
            ]),
            ParentNode("blockquote", [
                LeafNode(None, "According to all known laws of aviation, "),
                LeafNode(None, "there is no way a bee should be able to fly. "),
                LeafNode(None, "Its wings are too small to...")
            ]),
            ParentNode("p", [
                ParentNode("", [
                    LeafNode(None, "Above is a quote block. ")
                ]),
                ParentNode("", [
                    LeafNode(None, "And below is an ordered list with "),
                    LeafNode("i", "images"),
                    LeafNode(None, " and "),
                    LeafNode("i", "links"),
                    LeafNode(None, ".")
                ])
            ]),
            ParentNode("ol", [
                ParentNode("li", [
                    LeafNode(None, "This list item is "),
                    LeafNode("img", "", {"src": "https://stsci-opo.org/STScI-01GA76RM0C11W977JRHGJ5J26X.png", "alt": "an image of the Tarantula Nebula"})
                ]),
                ParentNode("li", [
                    LeafNode(None, "And this is a link "),
                    LeafNode("a", "to NASA website", {"href": "https://www.nasa.gov/"})
                ]),
                ParentNode("li", [
                    LeafNode(None, "This "),
                    LeafNode("code", "list item"),
                    LeafNode(None, " has a "),
                    LeafNode("i", "link"),
                    LeafNode(None, " to "),
                    LeafNode("a", "Wikipedia article about Hubble Space Telescope", {"href": "https://en.wikipedia.org/wiki/Hubble_Space_Telescope"}),
                    LeafNode(None, " and an "),
                    LeafNode("img", "", {"src": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/HST-SM4.jpeg/800px-HST-SM4.jpeg", "alt": "image of said telescope"})
                ])
            ]),
            ParentNode("p", [
                ParentNode("", [
                    LeafNode(None, "Finally, there is a code block with an example of a "),
                    LeafNode("code", "for"),
                    LeafNode(None, " loop function in "),
                    LeafNode("b", "Python"),
                    LeafNode(None, ".")
                ])
            ]),
            ParentNode("pre", [
                LeafNode("code", "for i in range(0, 10)<br>"),
                LeafNode("code", "    print(i)")
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), expected_output)

class TestExtractTitle(unittest.TestCase):
    def test_heading_only(self):
        markdown = "# This Is A Test Heading"
        expected_output = "This Is A Test Heading"
        self.assertEqual(extract_title(markdown), expected_output)

    def test_heading_and_paragraph(self):
        markdown = """\
# TEST HEADING

This is a paragraph with some words in it.
"""
        expected_output = "TEST HEADING"
        self.assertEqual(extract_title(markdown), expected_output)
    
    def test_heading_and_subheader(self):
        markdown = """\
# MAIN HEADING

## SUB HEADING

This is a paragraph with some words in it after a sub-heading.
"""
        expected_output = "MAIN HEADING"
        self.assertEqual(extract_title(markdown), expected_output)

    def test_heading_multiple_headings(self):
        markdown = """\
# First Heading

# MAIN HEADING AGAIN

# Another Heading
"""
        expected_output = "First Heading"

    def test_heading_exception(self):
        markdown = """\
This is just a markdown string without a heading.

```
some code
etc
```
"""
        with self.assertRaises(Exception):
            extract_title(markdown)
        

if __name__ == "__main__":
    unittest.main()