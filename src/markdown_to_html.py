from htmlnode import ParentNode, LeafNode
from mdblocks import BlockType
from textnode import TextNode, TextType
from inline_markdown import text_node_to_html_node, text_to_textnodes
import re

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in textnodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_html_node = ParentNode("div", [])

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            match = re.match(r"^(#{1,6}) (.*)", block)
            if match:
                level = len(match.group(1))
                text = match.group(2)
                children = text_to_children(text)
                node = ParentNode(f"h{level}", children)
                parent_html_node.children.append(node)
        elif block_type == BlockType.CODE:
            code_content = "\n".join(block.split('\n')[1:-1]) + "\n"
            code_node = text_node_to_html_node(TextNode(code_content, TextType.CODE))
            node = ParentNode("pre", [code_node])
            parent_html_node.children.append(node)
        elif block_type == BlockType.QUOTE:
            # Join quote lines with <br> and parse as inline markdown
            quote_lines = [line.lstrip("> ").rstrip() for line in block.split('\n')]
            quote_text = "<br>".join(quote_lines)
            children = text_to_children(quote_text)
            node = ParentNode("blockquote", children)
            parent_html_node.children.append(node)
        elif block_type == BlockType.UNORDERED_LIST:
            items = [line[2:].strip() for line in block.split('\n')]
            li_nodes = [ParentNode("li", text_to_children(item)) for item in items]
            node = ParentNode("ul", li_nodes)
            parent_html_node.children.append(node)
        elif block_type == BlockType.ORDERED_LIST:
            items = [re.sub(r"^\d+\. ", "", line).strip() for line in block.split('\n')]
            li_nodes = [ParentNode("li", text_to_children(item)) for item in items]
            node = ParentNode("ol", li_nodes)
            parent_html_node.children.append(node)
        else:  # BlockType.PARAGRAPH
            children = text_to_children(block.replace('\n', ' '))
            node = ParentNode("p", children)
            parent_html_node.children.append(node)

    return parent_html_node


def markdown_to_blocks(markdown):
    if not isinstance(markdown, str):
        raise ValueError("Input must be text")
    lines = markdown.split('\n')
    blocks = []
    current_block = []
    in_code_block = False

    for line in lines:
        is_heading = re.match(r"^#{1,6} ", line.strip())
        if line.strip().startswith("```"):
            if in_code_block:
                current_block.append(line)
                blocks.append('\n'.join(current_block).strip())
                current_block = []
                in_code_block = False
            else:
                if current_block:
                    blocks.append('\n'.join(current_block).strip())
                    current_block = []
                current_block.append(line)
                in_code_block = True
        elif in_code_block:
            current_block.append(line)
        elif line.strip() == "":
            if current_block:
                blocks.append('\n'.join(current_block).strip())
                current_block = []
        elif is_heading:
            if current_block:
                blocks.append('\n'.join(current_block).strip())
                current_block = []
            current_block.append(line)
            blocks.append('\n'.join(current_block).strip())
            current_block = []
        else:
            current_block.append(line)
    if current_block:
        blocks.append('\n'.join(current_block).strip())
    return [block for block in blocks if block]

def block_to_block_type(block):
    lines = block.split('\n')

    # Heading: 1-6 # followed by a space, only on the first line
    if re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING

    # Code block: starts and ends with ```
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    # Quote block: every line starts with >
    if all(line.strip().startswith(">") for line in lines if line.strip()):
        return BlockType.QUOTE

    # Unordered list: every line starts with "- "
    if all(line.strip().startswith("- ") for line in lines if line.strip()):
        return BlockType.UNORDERED_LIST

    # Ordered list: every line starts with incrementing number, dot, space
    ordered = True
    for idx, line in enumerate([l for l in lines if l.strip()]):
        match = re.match(r"^(\d+)\. ", line.strip())
        if not match or int(match.group(1)) != idx + 1:
            ordered = False
            break
    if ordered and len(lines) > 0 and lines[0].strip().startswith("1. "):
        return BlockType.ORDERED_LIST

    # Paragraph
    return BlockType.PARAGRAPH
