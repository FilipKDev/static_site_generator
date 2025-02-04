import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("h1", "this is a value", [], {"href": "https://www.google.com"})
        print(node)
        print("Props to HTML Method: " + node.props_to_html())

    def test_child(self):
        node_child = HTMLNode("p", "this is a child")
        node = HTMLNode("a", "this is a parent", [node_child], {"target": "_blank"})
        print(node)

    def test_children(self):
        node_child = HTMLNode("h1", "this is the first child")
        node_child_2 = HTMLNode("h2", "this is the second child", None, {"href": "https://www.google.com"})
        print("Props to HTML (Child 2): " + node_child_2.props_to_html())
        node = HTMLNode("html", "this is a parent", [node_child, node_child_2], {"name": "test"})
        print("Props to HTML (Parent Node): " + node.props_to_html())
        print(node)

    def test_empty(self):
        node = HTMLNode()
        print(node)

if __name__ == "__main__":
    unittest.main()