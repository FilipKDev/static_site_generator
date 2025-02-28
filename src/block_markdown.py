import re
from textnode import TextType, TextNode, text_node_to_html_node, text_to_textnodes
from leafnode import LeafNode
from parentnode import ParentNode

def extract_title(markdown):
    match = re.search(r"^#{1} .*", markdown, re.MULTILINE)
    if match:
        return match.group(0)[2:].strip()
    else:
        raise Exception("No header found")
        
def markdown_to_blocks(markdown):
    markdown_split = markdown.split("\n\n")
    string_list = []
    for string in markdown_split: 
        if string != "":
            string = string.strip("\n")
            string = string.strip()
            string_list.append(string)
    return string_list

def markdown_to_blocks_smart(markdown):
    markdown_split = markdown.split("\n\n")
    code_contents = check_for_code_blocks(markdown)
    code_contents_index = 0
    inside_code_block = False
    string_list = []
    for i in range(0, len(markdown_split)):
        string = markdown_split[i]
        if string != "" and string != "```" and not inside_code_block:
            string = string.strip("\n")
            string = string.strip()
            string_list.append(string)
        elif string == "```" and not inside_code_block:
            inside_code_block = True
            string_list.append("```" + code_contents[code_contents_index] + "\n```")
        elif string == "```" and inside_code_block:
            inside_code_block = False
            code_contents_index += 1
    return string_list

def check_for_code_blocks(markdown):
    split_by_code_lines = markdown.split("\n```")
    code_contents = []
    for i in range(0, len(split_by_code_lines)):
        if i % 2 == 1 and i < len(split_by_code_lines) - 1:
            code_contents.append(split_by_code_lines[i])
    return code_contents

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
    split_document = markdown_to_blocks_smart(markdown)
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
                block_nodes.extend(create_paragraph_node(block))
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
    i = 0
    for line in lines:
        line = re.sub(r"^([>])+", "", line)
        line = line.lstrip()
        if i != len(lines) - 1:
            line += " "
        children_nodes.extend(text_to_children(line))
        i += 1
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
        children_nodes.append(ParentNode("p", text_to_children(line)))
    return children_nodes

def text_to_children(line):
    children_nodes = []
    text_nodes = text_to_textnodes(line)
    for text_node in text_nodes:
        children_nodes.append(text_node_to_html_node(text_node))
    return children_nodes