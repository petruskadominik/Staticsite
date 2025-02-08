import unittest
from block_to_html import markdown_to_html_node


class TestMarkdown(unittest.TestCase):
    def test_markdown_to_html_node_basic(self):
        md = """# Heading 1

This is a paragraph. It **contains** some `simple` text.

## Heading 2

- Item 1 in an unordered list
- Item 2 in the list

1. Item 1 in an ordered list
2. Item 2 in the ordered *list*
3. Item 3 is **Bold**

> This is a blockquote. It might span across multiple lines."""
        node = markdown_to_html_node(md)
        print(node)
    
    def test_markdown_to_html_node_empty(self):
        md = ""
        node = markdown_to_html_node(md)
        #print("empty")
        #print(node)

    def test_markdown_empty_list(self):
        md = """- s
- d"""
        node = markdown_to_html_node(md)
        #print(node)

if __name__ == '__main__':
    unittest.main()