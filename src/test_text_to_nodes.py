import unittest
from text_to_nodes import text_to_text_nodes, markdown_to_blocks
from textnode import TextType, TextNode

class TestTextToTextNodes(unittest.TestCase):
    def test_everything_once(self):
        text = text_to_text_nodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, None, "https://i.imgur.com/fJRm4Vk.jpeg", "obi wan image"),  # Note the None for url
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertEqual(text, expected)

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
        
if __name__ == "__main__":
    unittest.main()