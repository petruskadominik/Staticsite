from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
        def __init__(self, text, text_type, url=None, src=None, alt=None):   
            self.text = text
            self.text_type = text_type
            self.url = url
            self.src = src  
            self.alt = alt

   #    def __eq__(self, compare):
   #         return self.text == compare.text and self.text_type == compare.text_type and self.url == compare.url
        
   #     def __repr__(self):
   #         return f"TextNode({self.text}, {self.text_type.value}, {self.url}, {self.src}, {self.alt})"
        
        def __repr__(self):
            if self.url:
                return f'TextNode("{self.text}", {self.text_type}, "{self.url}")'
            elif self.src:
                return f'TextNode("{self.text}", {self.text_type}, "{self.src}")'
            else:
                return f'TextNode("{self.text}", {self.text_type})'
            
        def __eq__(self, compare):
            if not isinstance(compare, TextNode):
                return False
            return (self.text == compare.text and 
                    self.text_type == compare.text_type and 
                    self.url == compare.url and
                    self.src == compare.src and
                    self.alt == compare.alt)