import unittest
from block_to_html import markdown_to_html_node
from generator import extract_title


class TestGenerator(unittest.TestCase):

    def test_generator_title(self):
        md = """# Heading 1

This is a paragraph. It **contains** some cd simple text.

## Heading 2

- Item 1 in an unordered list
- Item 2 in the list

1. Item 1 in an ordered list
2. Item 2 in the ordered *list*
3. Item 3 is **Bold**

> This is a blockquote. It might span across multiple lines."""
        title = extract_title(md)
        self.assertEqual(title, "Heading 1")

    def test_exception_case(self):
        with self.assertRaises(Exception):
            extract_title("some markdown without h1")


if __name__ == '__main__':
    unittest.main()