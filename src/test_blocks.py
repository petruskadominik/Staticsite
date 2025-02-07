import unittest
from blocks import markdown_to_blocks

class TestTextToTextNodes(unittest.TestCase):


    def test_md_to_block_basic(self):
        md = """# This is a heading


This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        expected = ['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\n* This is a list item\n* This is another list item']
        result = markdown_to_blocks(md)
        self.assertEqual(result, expected)

    def test_md_to_blocks_multiple_new_lines(self):
        md = """
# Heading

Some text

* List item 1
* List item 2"""
        expected = ['# Heading', 'Some text', '* List item 1\n* List item 2']
        result = markdown_to_blocks(md)
        self.assertEqual(result, expected)

    def test_md_to_blocks_whitespace(self):
        md = """   # Heading with spaces   

        Some indented text   
        more indented text   

    * List item"""
        expected = ['# Heading with spaces', 'Some indented text\nmore indented text', '* List item']
        result = markdown_to_blocks(md)
        self.assertEqual(result, expected)

    

    def test_md_to_blocks_empty_input(self):
        md = ""
        expected = []
        result = markdown_to_blocks(md)
        self.assertEqual(result, expected)

    def test_md_to_blocks_only_whitespace(self):
        md = """
        
            
        """
        expected = []
        result = markdown_to_blocks(md)
        self.assertEqual(result, expected)


    def test_md_to_blocks_complex_whitespace(self):
            md = """* First item
  * Indented item
* Last item"""
            expected = ['* First item\n  * Indented item\n* Last item']
            result = markdown_to_blocks(md)
            self.assertEqual(result, expected)


    def test_mixed_content(self):
        md = """# Header

    Regular paragraph
    here

* List item 1
  * Nested item
    * Deep nested
* Back to level 1"""
        expected = ['# Header', 'Regular paragraph\nhere', '* List item 1\n  * Nested item\n    * Deep nested\n* Back to level 1']
        result = markdown_to_blocks(md)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()

