from textnode import TextNode
from textnode import TextType

def main():
    text_node = TextNode("this is a text node", TextType.BOLD, "https://www.google.com")
    print(text_node)

main()