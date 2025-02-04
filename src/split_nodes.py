from textnode import TextType, TextNode
from markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        # Here's the key change - we'll process the text in chunks
        remaining_text = node.text
        
        while delimiter in remaining_text:  # Keep going while we find delimiters
            start_index = remaining_text.find(delimiter)
            if start_index == -1:
                break
                
            end_index = remaining_text.find(delimiter, start_index + len(delimiter))
            if end_index == -1:
                raise Exception("Closing delimiter not found")
            
            # Text before delimiter (if any)
            if start_index > 0:
                before_delimiters = TextNode(remaining_text[:start_index], TextType.TEXT)
                new_nodes.append(before_delimiters)
            
            # Text between delimiters
            between_delimiters = TextNode(
                remaining_text[start_index + len(delimiter):end_index], 
                text_type
            )
            new_nodes.append(between_delimiters)
            
            # Update remaining_text to be everything after this delimiter pair
            remaining_text = remaining_text[end_index + len(delimiter):]
        
        # Don't forget any remaining text after all delimiters are processed
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def split_single_node_image(node):
    images = extract_markdown_images(node.text)
    if not images:
        return [node]
    
    new_nodes = []
    remaining_text = node.text
    
    for image in images:
        # Split remaining_text on current image
        image_markdown = f"![{image[0]}]({image[1]})"
        sections = remaining_text.split(image_markdown, 1)
        
        # Add text before image if not empty
        if sections[0]:
            new_nodes.append(TextNode(text=sections[0], text_type=TextType.TEXT))
        
        # Add image node
        new_nodes.append(TextNode(text=image[0], text_type=TextType.IMAGE, src=image[1], alt=image[0]))
        
        # Update remaining_text for next iteration
        remaining_text = sections[1] if len(sections) > 1 else ""
    
    # Don't forget text after last image!
    if remaining_text:
        new_nodes.append(TextNode(text=remaining_text, text_type=TextType.TEXT))
    
    return new_nodes

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        result.extend(split_single_node_image(node))
    return result

def split_single_node_link(node):
    links = extract_markdown_links(node.text)
    if not links:
        return [node]
    
    new_nodes = []
    remaining_text = node.text
    
    for link in links:

        link_markdown = f"[{link[0]}]({link[1]})"
        sections = remaining_text.split(link_markdown, 1)
        
        if sections[0]:
            new_nodes.append(TextNode(text=sections[0], text_type=TextType.TEXT))
        
        new_nodes.append(TextNode(text=link[0], text_type=TextType.LINK, url=link[1]))
        
        remaining_text = sections[1] if len(sections) > 1 else ""
    
    if remaining_text:
        new_nodes.append(TextNode(text=remaining_text, text_type=TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        result.extend(split_single_node_link(node))
    return result