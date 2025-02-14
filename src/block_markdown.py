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

if __name__ == "__main__":
    text = """# This is a heading

  This is a paragraph of text. It has some **bold** and *italic* words inside of it.  




* This is the first list item in a list block
      * This is a list item
* This is another list item
"""
    print(markdown_to_blocks(text))