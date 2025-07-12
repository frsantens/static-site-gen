import unittest
from markdown_to_html import *
from mdblocks import BlockType


class TestMarkdownToBlocks(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])
    def test_single_paragraph(self):
        self.assertEqual(markdown_to_blocks("This is a paragraph."), ["This is a paragraph."])
    def test_multiple_paragraphs(self):
        self.assertEqual(
            markdown_to_blocks("First paragraph.\n\nSecond paragraph."),
            ["First paragraph.", "Second paragraph."]
        )
    def test_paragraph_with_newline(self):
        self.assertEqual(
            markdown_to_blocks("This is a paragraph.\n\nThis is another paragraph."),
            ["This is a paragraph.", "This is another paragraph."]
        )
    def test_paragraph_with_list(self):
        self.assertEqual(
            markdown_to_blocks("This is a paragraph.\n\n- Item 1\n- Item 2"),
            ["This is a paragraph.", "- Item 1\n- Item 2"]
        )
    def test_paragraph_with_code(self):
        self.assertEqual(
            markdown_to_blocks("This is a paragraph with `inline code`."),
            ["This is a paragraph with `inline code`."]
        )
    def test_paragraph_with_bold(self):
        self.assertEqual(
            markdown_to_blocks("This is a paragraph with **bold text**."),
            ["This is a paragraph with **bold text**."]
        )
    def test_paragraph_with_italic(self):
        self.assertEqual(
            markdown_to_blocks("This is a paragraph with _italic text_."),
            ["This is a paragraph with _italic text_."]
        )
    def test_paragraph_with_link(self):
        self.assertEqual(
            markdown_to_blocks("This is a paragraph with [a link](http://example.com)."),
            ["This is a paragraph with [a link](http://example.com)."]
        )
    def test_paragraph_with_image(self):
        self.assertEqual(
            markdown_to_blocks("This is a paragraph with ![an image](http://example.com/image.png)."),
            ["This is a paragraph with ![an image](http://example.com/image.png)."]
        )
    def test_paragraph_with_multiple_elements(self):
        self.assertEqual(
            markdown_to_blocks("This is a paragraph with **bold text**, _italic text_, and `inline code`."),
            ["This is a paragraph with **bold text**, _italic text_, and `inline code`."]
        )
    def test_paragraph_with_newline_and_list(self):
        self.assertEqual(
            markdown_to_blocks("This is a paragraph.\n\n- Item 1\n- Item 2\n\nThis is another paragraph."),
            ["This is a paragraph.", "- Item 1\n- Item 2", "This is another paragraph."]
        )
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):      
    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_heading_block(self):
        block = "# Heading Level 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_level_6(self):
        block = "###### Tiny Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_invalid_heading(self):
        block = "####### Not a valid heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block(self):
        block = "> First line\n> Second line\n> Third line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item one\n- Item two"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_order(self):
        block = "1. First\n2. Second\n4. Not in order"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)  # Should not be identified as ordered list

    def test_unordered_list_missing_dash(self):
        block = "- Item one\nItem two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block_mixed(self):
        block = "> Only first is a quote\nNot a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_not_closed(self):
        block = "```\nprint('oops')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_default(self):
        block = "Just a normal bit of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
  
  
class TestMarkdownToHtml(unittest.TestCase):
    def test_heading(self):
        md = "# Heading 1\n## Heading 2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2></div>",
        )

    def test_quote(self):
        md = "> This is a quote\n> Still a quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote<br>Still a quote</blockquote></div>",
        )      
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        
    def test_mixed_blocks(self):
        md= """
### Shopping
- Eggs
- Milk

Remember to buy everything!
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Shopping</h3><ul><li>Eggs</li><li>Milk</li></ul><p>Remember to buy everything!</p></div>",
        )