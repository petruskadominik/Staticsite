from textnode import TextType, TextNode
from markdown import extract_markdown_images, extract_markdown_links
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link

def text_to_text_nodes(text):
    nodes = [TextNode(text, TextType.TEXT)]    
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(nodes, "**", TextType.BOLD),
                      "*", TextType.ITALIC),
                        "`", TextType.CODE
            )
        )
    )

def markdown_to_blocks(markdown):
    remaining_text = markdown
    blocks = remaining_text.splitlines()
    result = []
    temp = ""
    for block in blocks:
        if block == "" and temp != "":
            result.append(temp)
            temp = ""
        else:
            if temp:
                if block.strip().startswith("*"):
                    temp = temp + '\n' + block.rstrip()
                else:
                    temp = temp + '\n' + block.strip()
            else:
                 temp = block.strip()
    if temp != "":
        result.append(temp)
   
    return result