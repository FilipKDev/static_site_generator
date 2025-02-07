from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, target):
        return self.text == target.text and self.text_type == target.text_type and self.url == target.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text).to_html()
        case TextType.BOLD:
            return LeafNode("b", text_node.text).to_html()
        case TextType.ITALIC:
            return LeafNode("i", text_node.text).to_html()
        case TextType.CODE:
            return LeafNode("code", text_node.text).to_html()
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": f"{text_node.url}"}).to_html()
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": f"{text_node.url}", "alt": f"{text_node.text}"}).to_html()
        case _:
            raise Exception("unknown text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            node_text_split = node.text.split(delimiter)
            delimiter_count = 0
            for char in node.text:
                if char == delimiter:
                    delimiter_count += 1
            if delimiter_count % 2 != 0:
                raise Exception("Invalid markdown syntax - no text enclosed by the delimiter")

            for i in range(0, len(node_text_split)):
                if i % 2 != 0:
                    new_nodes.append(TextNode(f"{node_text_split[i]}", text_type))
                else:
                    new_nodes.append(TextNode(f"{node_text_split[i]}", TextType.TEXT))
    return new_nodes  
