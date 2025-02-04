import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is also a text node", TextType.NORMAL)
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
        node = TextNode("This is a text node", TextType.IMAGES)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)



if __name__ == "__main__":
    unittest.main()