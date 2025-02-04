import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextType, TextNode

class TestHTMLNode(unittest.TestCase):
    def test_eq_same_propertiest(self):
        node = HTMLNode("a", "sample TEXT")
        node2 = HTMLNode("a", "sample TEXT")
        self.assertEqual(node, node2)
    
    def test_eq_none_properties(self):
        node = HTMLNode("h1", value=None)
        node2 = HTMLNode("h1")
        self.assertEqual(node, node2)

    def test_different_tag(self):
        node = HTMLNode("h1", "example text")
        node2 = HTMLNode("h2", "example text")
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(tag="a", props={"href": "https://www.example.com", "target": "_blank"})
        node2 = HTMLNode(tag="a", props={})
        self.assertNotEqual(node, node2)

    def test_props_empty(self):
        props = {}
        node = HTMLNode(tag="a", props=props)
        self.assertEqual(node.props_to_html(), "")

    def test_children_not_equal(self):
        child = HTMLNode(tag="b", value="sample text")
        node = HTMLNode(tag="a", value="example text", children=[child])
        node2 = HTMLNode(tag="a", value="example text")
        self.assertNotEqual(node, node2)
    
    def test_children_equal(self):
        child = HTMLNode(tag="b", value="sample text")
        node = HTMLNode(tag="a", value="example text", children=[child])
        node2 = HTMLNode(tag="a", value="example text", children=[child])
        self.assertEqual(node, node2)
        
    def test_nested_children(self):
        child = HTMLNode(tag="b", value="bold text")
        parent = HTMLNode(tag="div", children=[child])
        node2 = HTMLNode(tag="div", children=[HTMLNode(tag="b", value="bold text")])
        self.assertEqual(parent, node2)

    def test_leafnode_eq(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node, node2)
    
    def test_leafnode_not_eq(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertNotEqual(node, node2)
    
    def test_leafnode_props(self):
        props = {"href": "https://www.google.com"}
        node = LeafNode("a", "Click me!", props)
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node, node2)
    
    def test_leafnode_missing_value(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="p").to_html()

    def test_parent_nesting(self):
        child = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        child2 = LeafNode("b", "Bold text")
        child3 = ParentNode("p",[child, child2])
        child4 = ParentNode("p", [child3])
        child5 = LeafNode("i", "italic text")
        parent = ParentNode("p", [child4, child5])
        self.assertEqual(parent.to_html(), '<p><p><p><a href="https://www.google.com">Click me!</a><b>Bold text</b></p></p><i>italic text</i></p>')
        


    def test_parent_children(self):
        child = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        child2 = LeafNode("b", "Bold text")
        child3 = ParentNode("p", [child, child2])
        self.assertEqual(child3.to_html(), '<p><a href="https://www.google.com">Click me!</a><b>Bold text</b></p>')


    def test_parent_no_children(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), '<div></div>')


    def test_deeply_nested_parents(self):
        grandchild = LeafNode("span", "I am deep")
        child = ParentNode("div", [grandchild])
        parent = ParentNode("section", [child])
        self.assertEqual(parent.to_html(), '<section><div><span>I am deep</span></div></section>')

    def test_diverse_children(self):
        child1 = LeafNode("b", "Bold text")
        child2 = LeafNode(None, "Regular Text")
        child3 = LeafNode("i", "Italic text")
        parent = ParentNode("div", [child1, child2, child3])
        self.assertEqual(
            parent.to_html(),
            '<div><b>Bold text</b>Regular Text<i>Italic text</i></div>'
        )

    def test_tag_not_optional(self):
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [])
        self.assertEqual(str(context.exception), "Tag is NON-OPTIONAL")
    
    def test_children_not_optional(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None)
        self.assertEqual(str(context.exception), "Children are NON-OPTIONAL")

    def test_invalid_child_type(self):
        with self.assertRaises(TypeError) as context:
            ParentNode("div", [LeafNode("b", "Bold text"), "Invalid Child"]).to_html()
        self.assertEqual(str(context.exception), "Invalid child node type: <class 'str'>")

    def test_leafnode_malformed_props(self):
        with self.assertRaises(ValueError) as context:
            LeafNode("a", "Click me!", props="not-a-dict")
        self.assertEqual(str(context.exception), "Props must be a dictionary or None.")

    def test_parentnode_malformed_props(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", [], props=["not", "a", "dict"])
        self.assertEqual(str(context.exception), "Props must be a dictionary or None.")
        
    def test_parent_node_with_props(self):
        props = {"class": "container", "id": "main"}
        child = LeafNode("span", "Hello")
        parent = ParentNode("div", [child], props=props)
        expected = '<div class="container" id="main"><span>Hello</span></div>'
        self.assertEqual(parent.to_html(), expected)
    
    def test_parent_empty_with_props(self):
        props = {"class": "empty-container", "data-test": "true"}
        parent = ParentNode("div", [], props=props)

        expected = '<div class="empty-container" data-test="true"></div>'
        self.assertEqual(parent.to_html(), expected)
        
    def test_multiple_same_tag_parents(self):
        inner_p1 = ParentNode("p", [LeafNode("span", "First paragraph")])
        inner_p2 = ParentNode("p", [LeafNode("span", "Second paragraph")])
        inner_p3 = ParentNode("p", [LeafNode("span", "Third paragraph")])
        outer_p = ParentNode("p", [inner_p1, inner_p2, inner_p3])
        expected = '<p><p><span>First paragraph</span></p><p><span>Second paragraph</span></p><p><span>Third paragraph</span></p></p>'
        self.assertEqual(outer_p.to_html(), expected)

    def test_invalid_children_None(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None)

    def test_invalid_children_not_list(self):
        with self.assertRaises(ValueError):
            ParentNode("div", "Children are NON-OPTIONAL")

    def test_invalid_child_type_error(self):    
        with self.assertRaises(TypeError):
            ParentNode("div", [
                LeafNode("span", "valid"),
                123,  # invalid type
                LeafNode("p", "valid")
            ])

    def test_parent_empty_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)
    
    def test_parent_with_child_none_tag(self):
        
        parent = ParentNode("p", [
            LeafNode(None, "text")
        ])
        self.assertEqual(parent.to_html(), '<p>text</p>')
    
    def test_parent_mixed_children(self):
        parent = ParentNode("p", [
            LeafNode("b", "bold"),
            LeafNode(None, "normal"),
            LeafNode("i", "italic")
        ])
        self.assertEqual(parent.to_html(), '<p><b>bold</b>normal<i>italic</i></p>')

    def test_nested_parent_with_same_tag(self):
        parent = ParentNode("p", [
            ParentNode("p", [
                ParentNode("p", [LeafNode("span", "text")])
            ])
        ])

    def test_textnode_html_text(self):
        text_node = TextNode(text="Paragraf of text", text_type=TextType.TEXT)
        leaf_node = text_node_to_html_node(text_node)
        node2 = LeafNode(tag=None, value ="Paragraf of text")
        self.assertEqual(leaf_node, node2)

    def test_textnode_html_bold(self):
        text_node = TextNode(text="BOLD text", text_type=TextType.BOLD)
        leaf_node = text_node_to_html_node(text_node)
        node2 = LeafNode(tag='b', value="BOLD text")
        self.assertEqual(leaf_node, node2)

    def test_textnode_html_italic(self):
        text_node = TextNode(text="Italic text", text_type=TextType.ITALIC)
        leaf_node = text_node_to_html_node(text_node)
        node2 = LeafNode(tag='i', value="Italic text")
        self.assertEqual(leaf_node, node2)

    def test_textnode_html_code(self):
        text_node = TextNode(text="Code snippet", text_type=TextType.CODE)
        leaf_node = text_node_to_html_node(text_node)
        node2 = LeafNode(tag='code', value="Code snippet")
        self.assertEqual(leaf_node, node2)

    def test_textnode_html_link(self):
        text_node = TextNode(text="Click me!", text_type=TextType.LINK, url="https://www.google.com")
        leaf_node = text_node_to_html_node(text_node)
        node2 = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        self.assertEqual(leaf_node, node2)
    
    def test_textnode_html_image(self):
        text_node = TextNode(text="", text_type=TextType.IMAGE, src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhFZgqK1GycAkCqbiBwc3JM4r8MQW5VVzS_Xiujw6OjKeiLJnMDBW-9HvdGf8JD08SFAlQL51CA2q0llSRc-fReKYSddX9J8kb9W1Jnk1rF2TGQehsl1dN1UqOiZB8CAgVi55TCqmmBj-KG/s1600/Fiora_0.jpg", alt="Pretty picture")
        leaf_node = text_node_to_html_node(text_node)
        node2 = LeafNode(tag="img", value="", props={"src": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhFZgqK1GycAkCqbiBwc3JM4r8MQW5VVzS_Xiujw6OjKeiLJnMDBW-9HvdGf8JD08SFAlQL51CA2q0llSRc-fReKYSddX9J8kb9W1Jnk1rF2TGQehsl1dN1UqOiZB8CAgVi55TCqmmBj-KG/s1600/Fiora_0.jpg", "alt": "Pretty picture"})
        self.assertEqual(leaf_node, node2)

    def test_textnode_invalid_text_type_BOOBA(self):
        text_node = TextNode(text="Invalid type test", text_type="INVALID")
        with self.assertRaises(Exception):
            text_node_to_html_node(text_node)

    def test_textnode_link_no_url(self):
        text_node = TextNode(text="No URL", text_type=TextType.LINK)
        with self.assertRaises(Exception):
            text_node_to_html_node(text_node)

    def test_textnode_link_empty_string_url(self):
        text_node = TextNode(text="No URL", text_type=TextType.LINK, url ="")
        with self.assertRaises(Exception):
            text_node_to_html_node(text_node)

    def test_textnode_image_no_src_or_alt(self):
        text_node = TextNode(text="", text_type=TextType.IMAGE)
        with self.assertRaises(Exception):
            text_node_to_html_node(text_node)

    def test_textnode_image_empty_string_src(self):
        text_node = TextNode(text="", text_type=TextType.IMAGE, src = "", alt ="Alt for image")
        with self.assertRaises(Exception):
            text_node_to_html_node(text_node)

    def test_textnode_image_empty_string_alt(self):
        text_node = TextNode(text="", text_type=TextType.IMAGE, src ="https://www.google.com", alt ="")
        with self.assertRaises(Exception):
            text_node_to_html_node(text_node)

if __name__ == "__main__":
    unittest.main()