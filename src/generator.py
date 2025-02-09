from blocks import markdown_to_blocks 
from block_to_html import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
import os

def extract_title(markdown):
    lines = markdown.splitlines()
    if lines[0].startswith("#"):
        return lines[0].lstrip("# ")
    else:
        raise Exception("No title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        md = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    content = markdown_to_html_node(md)
    title = extract_title(md)

    result = template.replace('{{ Title }}', title)
    result = result.replace('{{ Content }}', content)

    directory = os.path.dirname(dest_path)
    os.makedirs(directory, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(result)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    src = os.listdir(dir_path_content)
    for item in src:
        if not item.startswith("."):
            source = os.path.join(dir_path_content, item)
            dest = os.path.join(dest_dir_path, item)
            if os.path.isfile(source) and source.endswith(".md"):
                dest = dest.replace(".md", ".html")            
                try:
                    generate_page(source, template_path, dest)
                except Exception as e:
                    print(f"Error generating page for {source}: {e}")
            else:
                generate_pages_recursive(source, template_path, dest)
        
