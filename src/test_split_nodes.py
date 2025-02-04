import unittest
from textnode import TextType, TextNode
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]
        )
    def test_split_italic(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ]
     )

    def test_no_delimiters(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [TextNode("This is just plain text", TextType.TEXT)]
        )

    def test_missing_delimiter(self):
        node = TextNode("This text has `no closing tick", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_delimited_sections(self):
        node = TextNode("Here is `one` and `two` codes", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("one", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.CODE),
                TextNode(" codes", TextType.TEXT),
            ]
        )
    def test_missing_end_delimiter(self):
        node = TextNode("Here is `one` and `two codes", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_link(self):
        nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",TextType.TEXT)]
        expected = [TextNode("This is text with a link ", TextType.TEXT), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.TEXT),TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),]
        self.assertEqual(split_nodes_link(nodes), expected)

    def test_split_nodes_image(self):
        nodes = [TextNode("This is a cool image![alt text](http://example.com/img.jpg) This is text with a link ![to boot dev](https://www.boot.dev) Yo", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is a cool image")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "alt text")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].src, "http://example.com/img.jpg")
        self.assertEqual(new_nodes[2].text, " This is text with a link ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "to boot dev")
        self.assertEqual(new_nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[3].src, "https://www.boot.dev")
        self.assertEqual(new_nodes[4].text, " Yo")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_split_nodes_image_no_images(self):
        nodes = [TextNode("This is just plain text", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(nodes,new_nodes)

    def test_split_nodes_link_image_at_start(self):
        nodes = [TextNode("[link text](https://example.com)rest of text", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(new_nodes[0].text, "link text")
        self.assertEqual(new_nodes[0].text_type, TextType.LINK)
        self.assertEqual(new_nodes[0].url, "https://example.com")
        self.assertEqual(new_nodes[1].text, "rest of text")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)
    
    def test_split_nodes_link_at_end(self):
        nodes = [TextNode("some text before [link text](https://example.com)", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(new_nodes[0].text, "some text before ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "link text")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://example.com")

    def test_split_nodes_consecutive_links(self):
        nodes = [TextNode("[link1](https://example1.com)[link2](https://example2.com)", TextType.TEXT)]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(new_nodes[0].text, "link1")
        self.assertEqual(new_nodes[0].text_type, TextType.LINK)
        self.assertEqual(new_nodes[0].url, "https://example1.com")
        self.assertEqual(new_nodes[1].text, "link2")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://example2.com")

    def test_split_nodes_empty_image_alt(self):
        nodes = [TextNode("before![](https://example.com/img.jpg)after", TextType.TEXT)]
        new_nodes = split_nodes_image(nodes)
        self.assertEqual(new_nodes[0].text, "before")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "")  # Empty alt text is valid
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].src, "https://example.com/img.jpg")
        self.assertEqual(new_nodes[2].text, "after")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
      


if __name__ == "__main__":
    unittest.main()