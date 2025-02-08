from blocks import markdown_to_blocks, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from text_to_nodes import text_to_text_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    if not blocks:
        return HTMLNode(tag="div", value=None, children=[], props={})
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
    return parent.to_html()

def heading_line_to_node(line):
    level = len(line) - len(line.lstrip('#'))
    line = line.lstrip('#').lstrip()
    text_nodes = text_to_text_nodes(line)
    kids = []
    for node in text_nodes:
            kids.append(text_node_to_html_node(node))
    return ParentNode(f"h{level}", children= kids)

def paragraph_block_to_node(block):
    text = "<br>".join(block.splitlines())
    text_nodes = text_to_text_nodes(text)
    kids = []
    for node in text_nodes:
            kids.append(text_node_to_html_node(node))
    return ParentNode(tag='p', children=kids)

def unordered_list_block_to_node(block):
    parents = []
    lines = block.splitlines()
    for line in lines:
        kids = []
        line = line.strip()
        line = line[2:].strip()
        text_nodes = text_to_text_nodes(line)
        for node in text_nodes:
            kids.append(text_node_to_html_node(node))
        parents.append(ParentNode(tag = 'li', children = kids))
    return ParentNode(tag = 'ul', children = parents)

def ordered_list_block_to_node(block):
    
    parents = []
    lines = block.splitlines()
    for line in lines:
        kids = []
        line = line.strip()
        line = line[2:].strip()
        text_nodes = text_to_text_nodes(line)
        for node in text_nodes:
            kids.append(text_node_to_html_node(node))
        parents.append(ParentNode(tag = 'li', children = kids))
    return ParentNode(tag = 'ol', children = parents)

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
    text_nodes = text_to_text_nodes(text)
    kids = []
    for node in text_nodes:
        kids.append(text_node_to_html_node(node))
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