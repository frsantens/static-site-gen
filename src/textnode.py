from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = ""
    BOLD = "**"
    ITALIC = "_"
    CODE = "'"
    LINK = ""
    IMAGE = ""

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(node1, node2):
        if(
            node1.text == node2.text and
            node1.text_type == node2.text_type and
            node1.url == node2.url
        ):
            return True
        return False
            
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK and text_node.url:
        return LeafNode("a", text_node.text, text_node.props_to_html())
    elif text_node.text_type == TextType.IMAGE and text_node.url:
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
    raise Exception("Not implemented")