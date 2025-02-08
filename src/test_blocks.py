import unittest
from blocks import markdown_to_blocks, block_to_block_type

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




    def test_block_types_headings(self):
        block1 = "# Heading"
        block2 = "## Heading"
        block3 = "### Heading"
        block4 = "#### Heading"
        block5 = "##### Heading"
        block6 = "###### Heading"
        block7 = "####### Heading"
        self.assertEqual(block_to_block_type(block1), "heading")
        self.assertEqual(block_to_block_type(block2), "heading")
        self.assertEqual(block_to_block_type(block3), "heading")
        self.assertEqual(block_to_block_type(block4), "heading")
        self.assertEqual(block_to_block_type(block5), "heading")
        self.assertEqual(block_to_block_type(block6), "heading")
        self.assertEqual(block_to_block_type(block7), "paragraph")

    def test_block_types_paragraph(self):
        block1 = "text"
        block2 = "######## aslo text"
        block3 = "````not code````"
        self.assertEqual(block_to_block_type(block1), "paragraph")
        self.assertEqual(block_to_block_type(block2), "paragraph")
        self.assertEqual(block_to_block_type(block3), "paragraph")

    
    def test_unordered_list(self):
        block = "* item one\n* item two\n- item three"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_ordered_list(self):
        block = "1. item one\n2. item two\n3. item three"
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_ordered_list_long(self):
        block = "1. item one\n2. item two\n3. item three\n4. item four\n5. item five\n6. item six\n7. item seven\n8. item eight\n9. item nine\n10. item ten\n11. item eleven\n12. item twelve"
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_invalid_ordered_list(self):
        block1 = "1. item one\n2. item two\n4. item four"
        self.assertEqual(block_to_block_type(block1), "paragraph")

    def test_quote_blocks(self):
        block = "> This is a quote\n> Multiple lines\n> In the quote"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_invalid_lists(self):
        block1 = "1.missing space"  # no space after period
        block2 = "* no space*\nafter asterisk"  # second line not a list item
        block3 = "-no space-after dash"  # no space after dash
        block4 = "* first line\njust text"  # second line not a list item
        self.assertEqual(block_to_block_type(block1), "paragraph")
        self.assertEqual(block_to_block_type(block2), "paragraph")
        self.assertEqual(block_to_block_type(block3), "paragraph")
        self.assertEqual(block_to_block_type(block4), "paragraph")

    def test_code_blocks(self):
        block1 = "```\nsome code\n```"
        block2 = "```python\ndef hello():\n    print('hello')\n```"
        self.assertEqual(block_to_block_type(block1), "code")
        self.assertEqual(block_to_block_type(block2), "code")

    def test_invalid_quotes(self):
        block1 = "> first line\nnot a quote line"  # second line missing >
        block2 = ">> double quote marks"  # multiple > characters
        self.assertEqual(block_to_block_type(block1), "paragraph")
        self.assertEqual(block_to_block_type(block2), "paragraph")
        

if __name__ == "__main__":
    unittest.main()

