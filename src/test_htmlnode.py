import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode
from textnode import TextType
from main import text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_props_to_html_return_type(self):
        props_argument = {"href": "https://www.google.com"}
        node = HTMLNode("h1", "this is a value", [], props_argument)
        self.assertIsNotNone(node.props_to_html())
        self.assertIsInstance(node.props_to_html(), str)

    def test_props_to_html_return_string(self):
        props_argument = {"href": "https://www.google.com"}
        node = HTMLNode("h1", "this is a value", [], props_argument)
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\"", "return string does not match expected output")

    def test_multiple_props_return_string(self):
        props_argument = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode("h1", "this is a value", [], props_argument)
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"", "return string does not match expected output")
                
    def test_child_argument(self):
        node_child = HTMLNode("p", "this is a child")
        node = HTMLNode("a", "this is a parent", [node_child], {"target": "_blank"})
        self.assertIsNotNone(node.children)
        self.assertIsInstance(node.children[0], HTMLNode)

    def test_repr_string(self):
        node = HTMLNode("b", "this is a value")
        self.assertIsInstance(node.__repr__(), str)

class TestLeafNode(unittest.TestCase):
    def test_empty(self):
        leaf_node = LeafNode(None, None)
        self.assertIsNone(leaf_node.tag)
        self.assertIsNone(leaf_node.value)

    def test_to_html_empty_tag(self):
        leaf_node = LeafNode(None, "test value test value")
        self.assertEqual(leaf_node.to_html(), leaf_node.value)

    def test_to_html(self):
        leaf_node = LeafNode("h1", "words words words words")
        self.assertIsInstance(leaf_node.to_html(), str)
        self.assertNotEqual(leaf_node.to_html(), leaf_node.value)

    def test_to_html_with_props(self):
        leaf_node = LeafNode("h1", "this test has props", {"href": "https://www.boot.dev", "name": "test"})
        self.assertIsInstance(leaf_node.to_html(), str)
        self.assertNotEqual(leaf_node.to_html(), leaf_node.value)
        self.assertEqual(leaf_node.to_html(), f"<{leaf_node.tag}{leaf_node.props_to_html()}>{leaf_node.value}</{leaf_node.tag}>")

    def test_to_html_exception(self):
        leaf_node = LeafNode("label", None)
        with self.assertRaises(ValueError):
            leaf_node.to_html()

class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        parent_node = ParentNode(None, [LeafNode("a", "test value")])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_no_children(self):
        parent_node = ParentNode("html", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_one_child(self):
        child = LeafNode(None, "test value")
        parent_node = ParentNode("p", [child])
        self.assertIsInstance(parent_node.to_html(), str)
        self.assertEqual(parent_node.to_html(), "<p>test value</p>")

    def test_to_html_two_children(self):
        child_1 = LeafNode("i", "italic test value")
        child_2 = LeafNode(None, "test value without tag")
        parent_node = ParentNode("p", [child_1, child_2])
        self.assertIsInstance(parent_node.to_html(), str)
        self.assertEqual(parent_node.to_html(), "<p><i>italic test value</i>test value without tag</p>")

    def test_to_html_parent_props(self):
        child_1 = LeafNode("b", "bold text")
        child_2 = LeafNode("i", "italic text")
        parent_node = ParentNode("h1", [child_1, child_2], {"href": "https://www.youtube.com/"})
        self.assertIsInstance(parent_node.to_html(), str)
        self.assertEqual(parent_node.to_html(), "<h1 href=\"https://www.youtube.com/\"><b>bold text</b><i>italic text</i></h1>")

    def test_to_html_children_props(self):
        child_1 = LeafNode("b", "bold text", {"name": "child 1"})
        child_2 = LeafNode("i", "italic text", {"name": "child 2"})
        parent_node = ParentNode("h1", [child_1, child_2])
        self.assertIsInstance(parent_node.to_html(), str)
        self.assertEqual(parent_node.to_html(), "<h1><b name=\"child 1\">bold text</b><i name=\"child 2\">italic text</i></h1>")

    def test_to_html_parent_children_props(self):
        child_1 = LeafNode("b", "bold text", {"name": "child 1"})
        child_2 = LeafNode("i", "italic text", {"name": "child 2"})
        parent_node = ParentNode("h1", [child_1, child_2], {"name": "parent"})
        self.assertIsInstance(parent_node.to_html(), str)
        self.assertEqual(parent_node.to_html(), "<h1 name=\"parent\"><b name=\"child 1\">bold text</b><i name=\"child 2\">italic text</i></h1>")

    def test_to_html_child_is_parent(self):
        child_1 = LeafNode("h1", "this is a leaf node value")
        child_parent = ParentNode("body", [child_1])
        parent_node = ParentNode("html", [child_parent])
        self.assertIsInstance(parent_node.to_html(), str)
        self.assertEqual(parent_node.to_html(), "<html><body><h1>this is a leaf node value</h1></body></html>")

    def test_to_html_child_is_parent_props(self):
        child_1 = LeafNode("h1", "this is a leaf node value", {"name": "child 1"})
        child_parent = ParentNode("body", [child_1], {"name": "parent node with child_1"})
        parent_node = ParentNode("html", [child_parent], {"name": "parent node with parent node with child_1"})
        self.assertIsInstance(parent_node.to_html(), str)
        self.assertEqual(
            parent_node.to_html(), 
            "<html name=\"parent node with parent node with child_1\"><body name=\"parent node with child_1\"><h1 name=\"child 1\">this is a leaf node value</h1></body></html>")

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_normal(self):
        text_node = TextNode("Standard text", TextType.NORMAL)
        self.assertEqual(text_node_to_html_node(text_node), text_node.text)

    def test_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        self.assertEqual(text_node_to_html_node(text_node), f"<b>{text_node.text}</b>")

    def test_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        self.assertEqual(text_node_to_html_node(text_node), f"<i>{text_node.text}</i>")

    def test_code(self):
        text_node = TextNode("Code text", TextType.CODE)
        self.assertEqual(text_node_to_html_node(text_node), f"<code>{text_node.text}</code>")

    def test_link(self):
        text_node = TextNode("link text", TextType.LINK, "https://link.link/")
        self.assertEqual(text_node_to_html_node(text_node), f"<a href=\"{text_node.url}\">{text_node.text}</a>")

    def test_images(self):
        text_node = TextNode("Image alt text", TextType.IMAGE, "https://www.google.co.uk/images/branding/googlelogo/2x/googlelogo_light_color_272x92dp.png")
        self.assertEqual(text_node_to_html_node(text_node), f"<img src=\"{text_node.url}\" alt=\"{text_node.text}\"></img>")

    def test_exception(self):
        text_node = TextNode("Something something", "nope")
        with self.assertRaises(Exception):
            text_node_to_html_node(text_node)

if __name__ == "__main__":
    unittest.main()