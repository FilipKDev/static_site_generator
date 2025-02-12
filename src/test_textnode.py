import unittest

from textnode import TextNode, TextType, split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is also a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("Text node with URL", TextType.ITALIC, "https://www.github.com")
        node2 = TextNode("Text node with URL", TextType.ITALIC, "https://www.github.com")
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("Text node with URL", TextType.ITALIC, "https://www.github.com")
        node2 = TextNode("Text node with URL", TextType.ITALIC, "https://www.gitlab.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_2(self):
        node = TextNode("Text node with URL", TextType.ITALIC, "https://www.github.com")
        node2 = TextNode("Text node with URL", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("Did you ever hear the tragedy of Darth Plagueis the Wise?", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_just_text_single_node(self):
        nodes = [TextNode("this is just text without delimiters", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.TEXT)
        self.assertEqual(new_nodes[0], TextNode("this is just text without delimiters", TextType.TEXT))

    def test_other_text_type(self):
        nodes = [TextNode("this is just text without delimiters", TextType.CODE)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.CODE)
        self.assertEqual(new_nodes[0], TextNode("this is just text without delimiters", TextType.CODE))

    def test_no_delimitires_in_node(self):
        nodes = [TextNode("this is just text without delimiters", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.CODE)
        self.assertEqual(new_nodes[0], TextNode("this is just text without delimiters", TextType.TEXT))

    def test_code_delimiter_single_node(self):
        nodes = [TextNode("this is text with a 'code block'", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "'", TextType.CODE)
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))

    def test_italic_delimiter_single_node(self):
        nodes = [TextNode("there are *italic words* in this text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        self.assertEqual(new_nodes[1], TextNode("italic words", TextType.ITALIC))

    def test_bold_delimiter_single_node(self):
        nodes = [TextNode("there are **bold words** in this text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes[1], TextNode("bold words", TextType.BOLD))

    def test_code_multiple_delimiters_single_node(self):
        nodes = [TextNode("this text has 'one code block' and then 'another code block'", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "'", TextType.CODE)
        expected_nodes = [
            TextNode("this text has ", TextType.TEXT), 
            TextNode("one code block", TextType.CODE),
            TextNode(" and then ", TextType.TEXT),
            TextNode("another code block", TextType.CODE),
            TextNode("", TextType.TEXT)]
        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])

    def test_italic_multiple_delimites_single_node(self):
        nodes = [TextNode("there are *italic words* and *more italic words* in this text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected_nodes = [
            TextNode("there are ", TextType.TEXT), 
            TextNode("italic words", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("more italic words", TextType.ITALIC),
            TextNode(" in this text", TextType.TEXT)]
        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])

    def test_bold_multiple_delimiters_single_node(self):
        nodes = [TextNode("there are **bold words** and **more bold words** in this text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("there are ", TextType.TEXT), 
            TextNode("bold words", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold words", TextType.BOLD),
            TextNode(" in this text", TextType.TEXT)]
        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])

    def test_code_multiple_nodes(self):
        nodes = [
            TextNode("First text node with a 'code block'", TextType.TEXT), 
            TextNode("Second text node with 'another code block'", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "'", TextType.CODE)
        expected_nodes = [
            TextNode("First text node with a ", TextType.TEXT), 
            TextNode("code block", TextType.CODE),
            TextNode("", TextType.TEXT),
            TextNode("Second text node with ", TextType.TEXT),
            TextNode("another code block", TextType.CODE),
            TextNode("", TextType.TEXT)]
        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])

    def test_italics_multiple_nodes(self):
        nodes = [
            TextNode("This text node has *italic* words", TextType.TEXT), 
            TextNode("Second text node also has words in *italic*", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected_nodes = [
            TextNode("This text node has ", TextType.TEXT), 
            TextNode("italic", TextType.ITALIC),
            TextNode(" words", TextType.TEXT),
            TextNode("Second text node also has words in ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("", TextType.TEXT)]
        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])

    def test_bold_multiple_nodes(self):
        nodes = [
            TextNode("This text node has **bold** words", TextType.TEXT), 
            TextNode("Second text node also has words in **bold**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This text node has ", TextType.TEXT), 
            TextNode("bold", TextType.BOLD),
            TextNode(" words", TextType.TEXT),
            TextNode("Second text node also has words in ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("", TextType.TEXT)]
        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected_nodes[i])

class TestExtractMarkdownImagesAndLinks(unittest.TestCase):
    def test_one_image(self):
        text = "This is a text with ![an F-16 fighter jet](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/F-16_June_2008.jpg/1200px-F-16_June_2008.jpg)"
        expected_output = [("an F-16 fighter jet", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/F-16_June_2008.jpg/1200px-F-16_June_2008.jpg")]
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_multiple_images(self):
        text = "This is a text with ![an F-16 fighter jet](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/F-16_June_2008.jpg/1200px-F-16_June_2008.jpg) and ![Godzilla](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Godzilla_%281954%29.jpg/1200px-Godzilla_%281954%29.jpg)"
        expected_output = [
            ("an F-16 fighter jet", "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/F-16_June_2008.jpg/1200px-F-16_June_2008.jpg"), 
            ("Godzilla", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Godzilla_%281954%29.jpg/1200px-Godzilla_%281954%29.jpg")]
        self.assertEqual(extract_markdown_images(text), expected_output)

    def test_one_link(self):
        text = "This is a text with a link [to Google](https://www.google.com/)"
        expected_output = [("to Google", "https://www.google.com/")]
        self.assertEqual(extract_markdown_links(text), expected_output)

    def test_multiple_links(self):
        text = "This is a text with a link [to Google](https://www.google.com/) and [to YouTube](https://www.youtube.com/)"
        expected_output = [
            ("to Google", "https://www.google.com/"),
            ("to YouTube", "https://www.youtube.com/")
        ]
        self.assertEqual(extract_markdown_links(text), expected_output)

    def test_image_and_link(self):
        text = "This is a text with ![an image of Godzilla](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Godzilla_%281954%29.jpg/1200px-Godzilla_%281954%29.jpg) and link [to Google](https://www.google.com/)"
        expected_images_output = [("an image of Godzilla", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Godzilla_%281954%29.jpg/1200px-Godzilla_%281954%29.jpg")]
        expected_link_output = [("to Google", "https://www.google.com/")]
        self.assertEqual(extract_markdown_images(text), expected_images_output)
        self.assertEqual(extract_markdown_links(text), expected_link_output)

if __name__ == "__main__":
    unittest.main()