from htmlnode import *
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0 and len(parts) > 1:
            raise ValueError("Delimiter split resulted in an odd number of parts, which is not allowed.")
        # Create TextNodes for each part, alternating between text and the specified text_type
        new_nodes.extend(
            TextNode(
                part,
                TextType.TEXT if i % 2 == 0 else text_type # Alternate between text and the specified type
                ) 
            for i, part in enumerate(parts)
            )
    return new_nodes