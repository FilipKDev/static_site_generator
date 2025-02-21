from textnode import TextNode
from textnode import TextType
import os
import shutil

def copy_files(source_path, destination_path):
    if os.path.exists(destination_path):
        print(f"removing {destination_path} and its contents")
        shutil.rmtree(destination_path)
    print(f"(re)creating {destination_path}")
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


def main():
    source_path = "/home/filip/workspace/github.com/FilipKDev/static_site_generator/static"
    destination_path = "/home/filip/workspace/github.com/FilipKDev/static_site_generator/public"
    copy_files(source_path, destination_path)

main()