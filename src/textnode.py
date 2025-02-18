from enum import Enum
from leafnode import LeafNode
import re

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
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": f"{text_node.url}"})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": f"{text_node.url}", "alt": f"{text_node.text}"})
        case _:
            raise Exception("unknown text type")

def extract_markdown_images(text):
    alt_text_list = re.findall(r"!\[(.*?)\]", text)
    url_list = re.findall(r"\((.*?)\)", text)
    image_tuples = []
    for i in range(0, len(alt_text_list)):
        image_tuple = (alt_text_list[i], url_list[i])
        image_tuples.append(image_tuple)
    return image_tuples

def extract_markdown_links(text):
    link_list = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link_list

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            delimiter_count = 0
            for char in node.text:
                if char == delimiter:
                    delimiter_count += 1
            if delimiter_count % 2 != 0:
                raise Exception("Invalid markdown syntax - no text enclosed by the delimiter")

            node_text_split = node.text.split(delimiter)
            for i in range(0, len(node_text_split)):
                if i % 2 != 0:
                    new_nodes.append(TextNode(f"{node_text_split[i]}", text_type))
                else:
                    new_nodes.append(TextNode(f"{node_text_split[i]}", TextType.TEXT))
    return new_nodes  

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not node.text:
            continue

        node_images = extract_markdown_images(node.text)
        node_text = node.text

        if not node_images or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        for i in range(0, len(node_images)):
            node_text_split = node_text.split(f"![{node_images[i][0]}]({node_images[i][1]})", 1)
            if node_text_split[0] != "":
                new_nodes.append(TextNode(f"{node_text_split[0]}", TextType.TEXT))
            new_nodes.append(TextNode(f"{node_images[i][0]}", TextType.IMAGE, f"{node_images[i][1]}"))
            if i == len(node_images) - 1 and node_text_split[1] != "":
                new_nodes.append(TextNode(f"{node_text_split[1]}", TextType.TEXT))
            node_text = node_text_split[1]
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not node.text:
            continue

        node_links = extract_markdown_links(node.text)
        node_text = node.text

        if not node_links or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        for i in range(0, len(node_links)):
            node_text_split = node_text.split(f"[{node_links[i][0]}]({node_links[i][1]})", 1)
            if node_text_split[0] != "":
                new_nodes.append(TextNode(f"{node_text_split[0]}", TextType.TEXT))
            new_nodes.append(TextNode(f"{node_links[i][0]}", TextType.LINK, f"{node_links[i][1]}"))
            if i == len(node_links) - 1 and node_text_split[1] != "":
                new_nodes.append(TextNode(f"{node_text_split[1]}", TextType.TEXT))
            node_text = node_text_split[1]
    return new_nodes

def text_to_textnodes(text):
    return split_nodes_image(split_nodes_link(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD), "*", TextType.ITALIC), "`", TextType.CODE)))

if __name__ == "__main__":
    text = """\
`Some code at the start` and 
*italic* text and 
then (a link)(https://google.com/)"""
    print(f"{text_to_textnodes(text)}")