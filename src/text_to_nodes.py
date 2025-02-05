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

def test_bold_only(self):
    text = "This is **bold** text"
    nodes = text_to_text_nodes(text)
    expected = [
        TextNode("This is ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" text", TextType.TEXT)
    ]
    self.assertEqual(nodes, expected)

def test_code_and_italic(self):
    text = "Here is `code` and *italic*"
    nodes = text_to_text_nodes(text)
    expected = [
        TextNode("Here is ", TextType.TEXT),
        TextNode("code", TextType.CODE),
        TextNode(" and ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC)
    ]
    self.assertEqual(nodes, expected)

def test_image_only(self):
    text = "![alt text](https://example.com/img.jpg)"
    nodes = text_to_text_nodes(text)
    expected = [
        TextNode("alt text", TextType.IMAGE, None, "https://example.com/img.jpg", "alt text")
    ]
    self.assertEqual(nodes, expected)