from textnode import TextType, TextNode
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

