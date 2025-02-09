
from block_to_html import markdown_to_html_node
import os
import shutil

def main():
    base_dir = "/home/domino/workspace/github.com/petruskadominik/Staticsite"
    public_dir = os.path.join(base_dir, "public")
    static_dir = os.path.join(base_dir, "static")
    
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    os.mkdir(public_dir)

    shutil.copy(f"{static_dir}/*", public_dir)

main()

