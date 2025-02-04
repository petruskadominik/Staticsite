import unittest
from markdown import extract_markdown_images, extract_markdown_links

class TestMarkdown(unittest.TestCase):
    def test_extract_images(self):
        text = "![alt text](http://example.com/img.jpg)"
        expected = [("alt text", "http://example.com/img.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)


    def test_extreact_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_image_no_image(self):
        text = 'to boot dev'
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)


    def test_extreact_links_no_links(self):
        text = 'to boot dev'
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_images_missing_link(self):
        text = "[link](missing_url)"
        expected = [('link', 'missing_url')]
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_extract_iamges_open_bracket(self):
        text = '![alt textto boot dev'
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_images_with_brackets_limitation(self):
        """Note: Current implementation doesn't support nested brackets in alt text"""
        text = "![simple alt text](http://example.com/img.jpg)"
        expected = [("simple alt text", "http://example.com/img.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)
        

    


if __name__ == '__main__':
    unittest.main()