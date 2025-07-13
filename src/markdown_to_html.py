from genericpath import isfile
from pydoc import isdata
from htmlnode import ParentNode, BlockType
from textnode import TextNode, TextType
from inline_markdown import text_node_to_html_node, text_to_textnodes
import re
import os

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

def extract_title(markdown):
    pattern = r"^# (.*)"
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING and block.startswith('# '):
            match = re.match(r"^# (.*)", block)
            if match:
                return match.group(1).strip()
    raise Exception("no h1 header found")

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path, encoding="utf_8") as f:
        markdown = f.read()
    with open(template_path, encoding="utf_8") as f:
        template = f.read()
    parent_node = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    full_page = template.replace( '{{ Title }}', title ).replace( '{{ Content }}', parent_node)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    if os.path.isfile(os.path.abspath(from_path)):
        with open(os.path.abspath(dest_path), "w") as f:
            f.write(full_page)

    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isdir(dir_path_content):
        rel_src_paths = os.listdir(dir_path_content)
    else:
        rel_src_paths = [dir_path_content]
    for src in rel_src_paths:
        if  dir_path_content != src:
            abs_src = os.path.join(dir_path_content,src)
        else: abs_src = src
        nested_dest_dir = os.path.join(dest_dir_path,src.replace(".md",".html"))
        print('nested destination path (should be .html) : ', nested_dest_dir)
        
        if os.path.isfile(abs_src) and abs_src.endswith('.md'):
            generate_page(abs_src, template_path, nested_dest_dir)
            continue
        elif os.path.isdir(abs_src):
            generate_pages_recursive(abs_src, template_path, nested_dest_dir)
            continue
    