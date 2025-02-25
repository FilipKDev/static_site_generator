from textnode import TextNode, TextType
from block_markdown import extract_title, markdown_to_html_node
from parentnode import ParentNode
import os
import shutil

def copy_files(source_path, destination_path):
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)
    for item in os.listdir(source_path):
        new_source_path = os.path.join(source_path, item)
        new_destination_path = os.path.join(destination_path, item)
        if os.path.isfile(new_source_path):
            print(f"Copying {item} from {source_path} to {destination_path}")
            shutil.copy(new_source_path, new_destination_path)
        else:
            print(f"looking in {new_source_path}")
            if not os.path.exists(new_destination_path):
                os.mkdir(new_destination_path)
            copy_files(new_source_path, new_destination_path)
    return

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown = read_markdown(from_path)
    markdown_html_node = markdown_to_html_node(markdown)
    title = extract_title(markdown)

    template = read_template(template_path)
    webpage = template.replace("{{ Title }}", title)
    webpage = webpage.replace("{{ Content }}", markdown_html_node.to_html())

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    webpage_file = open(os.path.join(dest_path, "index.html"), "x")
    webpage_file.write(webpage)
    webpage_file.close()

def read_markdown(from_path):
    if not os.path.exists(from_path):
        raise Exception("Invalid path")
    for file in os.listdir(from_path):
        if os.path.isfile(os.path.join(from_path, file)) and file[-3:] == ".md":
            markdown = open(os.path.join(from_path, file)).read()
            return markdown

def read_template(template_path):
    if not os.path.exists(template_path):
        raise Exception("Invalid path")
    for file in os.listdir(template_path):
        if os.path.isfile(os.path.join(template_path, file)) and file[-5:] == ".html":
            template = open(os.path.join(template_path, file)).read()
            return template

def main():
    from_path = "/home/filip/workspace/github.com/FilipKDev/static_site_generator/content"
    template_path = "/home/filip/workspace/github.com/FilipKDev/static_site_generator"
    dest_path = "/home/filip/workspace/github.com/FilipKDev/static_site_generator/public"
    
    if os.path.exists(dest_path):
        print(f"removing {dest_path} and its contents")
        shutil.rmtree(dest_path)
    generate_page(from_path, template_path, dest_path)
    copy_files("/home/filip/workspace/github.com/FilipKDev/static_site_generator/static", dest_path)

main()