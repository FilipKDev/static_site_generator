import re
from textnode import TextType, TextNode, text_node_to_html_node, text_to_textnodes
from leafnode import LeafNode
from parentnode import ParentNode

def markdown_to_blocks(markdown):
    markdown_split = markdown.split("\n\n")
    string_list = []
    for string in markdown_split:
        if string != "":
            string = string.strip("\n")
            string = string.strip()
            string_list.append(string)
    return string_list

def block_to_block_type(markdown):
    if re.match(r"#{1,6}(?= )", markdown):
        return "heading"
    elif re.match(r"^`{3}[\s\S]*`{3}$", markdown):
        return "code"
    elif re.fullmatch(r"^(>.*\n?)*$", markdown, re.MULTILINE):
        return "quote"
    elif re.fullmatch(r"^([-*] .*\n?)*$", markdown, re.MULTILINE):
        return "unordered list"
    elif re.fullmatch(r"^([0-9]+. .*\n?)*$", markdown, re.MULTILINE):
        return "ordered list"
    else:
        return "normal"

def markdown_to_html_node(markdown):
    split_document = markdown_to_blocks(markdown)
    block_nodes = []
    for block in split_document:
        block_type = block_to_block_type(block)
        match block_type:
            case "heading": 
                block_nodes.append(create_header_node(block))
            case "code":
                block_nodes.append(create_code_node(block))
            case "quote":
                block_nodes.append(create_quote_node(block))
            case "unordered list":
                block_nodes.append(create_unordered_list_node(block))
            case "ordered list":
                block_nodes.append(create_ordered_list_node(block))
            case "normal":
                block_nodes.append(create_paragraph_node(block))
    return ParentNode("div", block_nodes)
            
def create_header_node(block):
    header_match = re.match(r"^(#+) ", block)
    hash_count = len(list(header_match.group(1)))
    children_nodes = text_to_children(block[hash_count+1:])
    return ParentNode(f"h{hash_count}", children_nodes)

def create_code_node(block): 
    lines = re.split(r"(\n)", block[4:-4])
    children_nodes = []
    for line in lines:
        if line != "\n":
            text_node = TextNode(line, TextType.CODE)
            children_nodes.append(text_node_to_html_node(text_node))
        else:
            children_nodes[-1].value += "<br>"       
    return ParentNode("pre", children_nodes)

def create_quote_node(block):
    lines = block.split("\n")
    children_nodes = []
    for line in lines:
        line = re.sub(r"^([>])+ ", "", line)
        children_nodes.extend(text_to_children(line))
    return ParentNode("blockquote", children_nodes)

def create_unordered_list_node(block):
    lines = block.split("\n")
    children_nodes = []
    for line in lines:
        children_nodes.append(ParentNode("li", text_to_children(line[2:]))) 
    return ParentNode("ul", children_nodes)

def create_ordered_list_node(block):
    lines = block.split("\n")
    children_nodes = []
    for line in lines:
        line = re.sub(r"^([0-9])+. ", "", line)
        children_nodes.append(ParentNode("li", text_to_children(line)))
    return ParentNode("ol", children_nodes)

def create_paragraph_node(block):
    lines = block.split("\n")
    children_nodes = []
    for line in lines:
        children_nodes.append(ParentNode("", text_to_children(line)))
    return ParentNode("p", children_nodes)

def text_to_children(line):
    children_nodes = []
    text_nodes = text_to_textnodes(line)
    for text_node in text_nodes:
        children_nodes.append(text_node_to_html_node(text_node))
    return children_nodes

if __name__ == "__main__":
    heading_text = """\
#### HEADING *BOLD* WORDS
"""
    code_text = """\
```
TEST CODE
test code
```
"""
    quote_text = """\
> Quote 1
> Quote 2
>> QUOTE 3
>>>>> QUOTE 4
"""
    unordered_text = """\
* Unordered list item
* Unordered **list** item
"""
    ordered_text = """\
99. Ordered list item 1
100. **Ordered** list *item* 2
"""
    paragraph_text = """\
Test testing **bold text** and *italic text*
"""
    test_1 = """\
### Search websites

1. [Google](https://www.google.co.uk/)
2. [Bing](https://www.bing.com/)
3. [DuckDuckGo](https://duckduckgo.com/)
"""
    markdown_to_html_node(test_1)