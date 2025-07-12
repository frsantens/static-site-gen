from textnode import TextNode, TextType
from htmlnode import LeafNode
import re

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
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE and text_node.url:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise Exception("Not implemented")

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    # Order: images, links, code, bold, italic
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes

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
        if len(parts) % 2 == 0:
            raise ValueError("Unbalanced delimiter in text node.")
        for i, part in enumerate(parts):
            # Only add non-empty nodes, except for the middle ones
            if i % 2 == 0:
                if part != "" or (i == 0 and len(parts) == 1):
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def split_nodes_image(old_nodes): 
    new_nodes = []
    pattern = r'!\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(([^)]*)\)'
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)
        if not images:
            new_nodes.append(node)
            continue

        # Build a list of the full markdown image strings
        image_markdowns = [f"![{alt}]({url})" for alt, url in images]
        # Split the text on each image markdown, preserving order
        parts = re.split(pattern, text)
        # parts will alternate: [text, alt1, url1, text, alt2, url2, text, ...]
        i = 0
        while i < len(parts):
            # Text before image
            if parts[i]:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            if i + 2 < len(parts):
                alt = parts[i+1]
                url = parts[i+2]
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            i += 3
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    pattern = r'(?<!!)\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(([^)]*)\)'
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)
        if not links:
            new_nodes.append(node)
            continue

        # Build a list of the full markdown link strings
        link_markdowns = [f"[{txt}]({url})" for txt, url in links]
        # Split the text on each link markdown, preserving order
        parts = re.split(pattern, text)
        # parts will alternate: [text, link_text1, url1, text, link_text2, url2, text, ...]
        i = 0
        while i < len(parts):
            # Text before link
            if parts[i]:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            if i + 2 < len(parts):
                link_text = parts[i+1]
                url = parts[i+2]
                new_nodes.append(TextNode(link_text, TextType.LINK, url))
            i += 3
    return new_nodes

def extract_markdown_images(text):
    # Allows one level of nested brackets in alt text
    pattern = r'!\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(([^)]*)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    # Allows one level of nested brackets in link text
    pattern = r'(?<!!)\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(([^)]*)\)'
    matches = re.findall(pattern, text)
    return matches

