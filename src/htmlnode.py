from textnode import TextType, TextNode

class HTMLNode:
    def __init__(self,tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else None
        if props is not None and not isinstance(props, dict):
            raise ValueError("Props must be a dictionary or None.")
        self.props = {} if props is None else props

    def to_html(self):
        raise NotImplementedError   
    
    def props_to_html(self):
        output = ""
        if self.props:
            for key, value in self.props.items():
                output += f' {key}="{value}"'
        return output
    
    def __eq__(self, compare):
        if not isinstance(compare, HTMLNode):
            return False
        return (self.tag == compare.tag and 
                self.value == compare.value and 
                (self.children or []) == (compare.children or [])and 
                (self.props or {}) == (compare.props or {}))

    def __repr__(self):
        try:
            if self.children is None:
                children_repr = "None"
            elif any(child is None for child in self.children):
                children_repr = "[Invalid child: None]"
            else:
                children_repr = ", ".join([child.tag or "text" for child in self.children])
            return f"HTMLNode(tag={self.tag}, value={self.value}, children=[{children_repr}], props={self.props})"
        except Exception as e:
            return f"HTMLNode(DEBUG ERROR: {e})"
    
class LeafNode(HTMLNode):
    def __init__(self,tag=None, value=None, props=None):
        super().__init__(tag, value, None, props=props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
    
    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        # Compare only relevant attributes for a LeafNode
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.props == other.props
        )
    
        

class ParentNode(HTMLNode):
    def __init__(self,tag, children,props=None):
        if props is not None and not isinstance(props, dict):
            raise ValueError("Props must be a dictionary or None.")
        if tag == None:
            raise ValueError("Tag is NON-OPTIONAL")
        if children is None:
            raise ValueError("Children are NON-OPTIONAL")
        if not isinstance(children, list):
            raise ValueError("Children are NON-OPTIONAL")
        for child in children:
            if not isinstance(child, HTMLNode):
                raise TypeError(f"Invalid child node type: {type(child)}")
        super().__init__(tag, None, children, props)
        self.props = {} if props is None else props
        
    def __repr__(self):
        children_repr = ', '.join(repr(child) for child in self.children) if self.children else "[]"
        return f"HTMLNode(tag={self.tag}, value={repr(self.value)}, children=[\n{children_repr}], props={self.props})"
        
        
    def to_html(self):
        
        children_to_html = ""
        for child in self.children:
            children_to_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_to_html}</{self.tag}>"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag = 'b', value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag = 'i', value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag = 'code', value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        if not text_node.url:
            raise Exception("TextType.LINK must include a 'url'.")
        return LeafNode(tag = 'a', value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        if not text_node.src:
            raise Exception("TextType.IMAGE must include a 'src'.")
        if not text_node.alt:
            raise Exception("TextType.IMAGE must include an 'alt'.")        
        return LeafNode(tag = 'img', value="", props={"src": text_node.src, "alt": text_node.alt})
    else:
        raise Exception("Invalid TextType")