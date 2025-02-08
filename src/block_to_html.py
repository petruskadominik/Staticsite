from blocks import markdown_to_blocks, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_nodes import text_to_text_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        if block_to_block_type(block) == "heading":
            lines = block.splitlines()
            for line in lines:
                block_nodes.append(heading_line_to_node(line))
        elif block_to_block_type(block) == "paragraph":
            block_nodes.append(paragraph_block_to_node(block))
        elif block_to_block_type(block) == "unordered_list":
            block_nodes.append(unordered_list_block_to_node(block))
        elif block_to_block_type(block) == "ordered_list":
            block_nodes.append(ordered_list_block_to_node(block))
        elif block_to_block_type(block) == "quote":
            block_nodes.append(blockquote_block_to_node(block))
        elif block_to_block_type(block) == "code":
            block_nodes.append(code_block_to_node(block))
    parent = ParentNode(tag = 'div', children = block_nodes)
    return parent

def heading_line_to_node(line):
    level = len(line) - len(line.lstrip('#'))
    return LeafNode(f"h{level}", line.lstrip('#').lstrip())

def paragraph_block_to_node(block):
    text = "<br>".join(block.splitlines())
    return LeafNode(tag='p', value=text)

def unordered_list_block_to_node(block):
    kids = []
    lines = block.splitlines()
    for line in lines:
        line = line.strip()
        line = line[2:].strip()
        kids.append(LeafNode(tag = 'li', value = line))
    return ParentNode(tag = 'ul', children = kids)

def ordered_list_block_to_node(block):
    kids = []
    lines = block.splitlines()
    for line in lines:
        line = line.strip()
        line = line[2:].strip()
        kids.append(LeafNode(tag = 'li', value = line))
    return ParentNode(tag = 'ol', children = kids)

def blockquote_block_to_node(block):
    lines = block.splitlines()
    text = ""
    for line in lines:
        line = line.strip()
        line = line.strip("> ")
        if text:
            text += " " + line
        else:
            text = line
    kids = [LeafNode(tag="p", value = text)]
    return ParentNode(tag = 'blockquote', children = kids)

def code_block_to_node(block):
    lines = block.splitlines()
    text = ""
    rows = len(lines)
    for i in range(1,rows -1):
        if text:
            text += "\n" + lines[i]
        else:
            text = lines[i]
    child = [LeafNode(tag = 'code', value = text)]
    return ParentNode(tag = 'pre', children = child)


    






md = """
# Heading 1

This is the first paragraph.
It spans multiple lines,
but it’s still a single paragraph.

## Heading 2

This is another paragraph.
It is shorter.

### Heading 3

- Item 1
- Item 2

1. Item 1
2. Item 2
3. Item 3

> This is a blockquote.
> Over multiple
> lines

Another paragraph to end with

```
This is a code block
It preserves whitespace
And can span multiple lines
```

```
print("here are some ```backticks``` in code")
def func():
    return "test"
```
"""


node = markdown_to_html_node(md)
print(node)