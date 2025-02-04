from textnode import TextNode
from textnode import TextType

def main():
    text_node = TextNode("this is a text node", TextType.BOLD, "https://www.google.com")
    text_node_string = text_node.__repr__()
    print(text_node_string)

main()