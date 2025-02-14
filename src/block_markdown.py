import re

def markdown_to_blocks(markdown):
    markdown_split = markdown.split("\n\n")
    string_list = []
    for string in markdown_split:
        lines = []
        for line in string.split("\n"):
            lines.append(line.strip())
        if string != "":
            string_list.append("\n".join(lines).strip("\n"))
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



if __name__ == "__main__":
    text = """\
1. list1
> list2
3. list3"""
    block_to_block_type(text)