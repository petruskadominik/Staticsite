
from block_to_html import markdown_to_html_node
import os
import shutil

def recursive_copy(src, dest):
    source = os.listdir(src)
    for file in source:
        path = os.path.join(src, file)
        if os.path.isfile(path):
            print(f"Copping {file} to {dest}")
            shutil.copy(path, dest)
        else:
            dir = os.path.join(dest, file)
            os.mkdir(dir)
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

main()


