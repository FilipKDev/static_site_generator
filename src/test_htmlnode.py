import unittest

from htmlnode import HTMLNode
from leafnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None, "tag is not empty")
        self.assertEqual(node.value, None, "value is not empty")
        self.assertEqual(node.children, None, "children is not empty")
        self.assertEqual(node.props, None, "props is not empty")

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
        leaf_node = LeafNode("h1", "this test has props", None, {"href": "https://www.boot.dev", "name": "test"})
        self.assertIsInstance(leaf_node.to_html(), str)
        self.assertNotEqual(leaf_node.to_html(), leaf_node.value)

    def test_to_html_exception(self):
        leaf_node = LeafNode("label", None)
        with self.assertRaises(ValueError):
            leaf_node.to_html()

if __name__ == "__main__":
    unittest.main()