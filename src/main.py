from generator import generate_pages_recursive
from block_to_html import markdown_to_html_node
import os
import shutil

def recursive_copy(src, dest):
    source = os.listdir(src)
    for file in source:
        if not file.startswith("."):
            path = os.path.join(src, file)
            if os.path.isfile(path):
                print(f"Copying {file} to {dest}")
                try:
                    shutil.copy(path, dest)
                except Exception as e:
                    print(f"Failed to copy {path}: {e}")
            elif os.path.isdir(path):
                dir = os.path.join(dest, file)
                os.makedirs(dir, exist_ok=True)
                recursive_copy(path, dir)

def main():
    base_dir = "/home/domino/workspace/github.com/petruskadominik/Staticsite"
    public_dir = os.path.join(base_dir, "public")
    static_dir = os.path.join(base_dir, "static")
    
    if os.path.exists(public_dir):
        print(f"Deleting {public_dir}")
        shutil.rmtree(public_dir)

    print(f"Creating dir {public_dir}")
    os.mkdir(public_dir)

    recursive_copy(static_dir, public_dir)

    content_dir = os.path.join(base_dir, "content")
    template_path = os.path.join(base_dir, "template.html")

    generate_pages_recursive(content_dir, template_path, public_dir)

main()


