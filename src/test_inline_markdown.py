from inline_markdown import *
from textnode import TextNode, TextType
import unittest

class TestInlineMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_images_no_match(self):
        self.assertEqual(extract_markdown_images("No images here!"), [])

    def test_images_multiple(self):
        text = "![img1](url1) and ![img2](url2)"
        self.assertEqual(
            extract_markdown_images(text),
            [("img1", "url1"), ("img2", "url2")]
        )

    def test_images_empty_alt(self):
        self.assertEqual(
            extract_markdown_images("![](url)"),
            [("", "url")]
        )

    def test_images_empty_url(self):
        self.assertEqual(
            extract_markdown_images("![alt]()"),
            [("alt", "")]
        )

    def test_images_nested_brackets(self):
        # Should not match nested brackets in alt text
        self.assertEqual(
            extract_markdown_images("![alt[inner]](url)"),
            [("alt[inner]", "url")]
        )

    def test_links_no_match(self):
        self.assertEqual(extract_markdown_links("No links here!"), [])

    def test_links_multiple(self):
        text = "[link1](url1) and [link2](url2)"
        self.assertEqual(
            extract_markdown_links(text),
            [("link1", "url1"), ("link2", "url2")]
        )

    def test_links_empty_text(self):
        self.assertEqual(
            extract_markdown_links("[](url)"),
            [("", "url")]
        )

    def test_links_empty_url(self):
        self.assertEqual(
            extract_markdown_links("[text]()"),
            [("text", "")]
        )

    def test_links_escaped_image(self):
        # Should not match image syntax as a link
        self.assertEqual(
            extract_markdown_links("![notalink](url)"),
            []
        )

    def test_links_nested_brackets(self):
        # Should not match nested brackets in link text
        self.assertEqual(
            extract_markdown_links("[text[inner]](url)"),
            [("text[inner]", "url")]
        )
        


class TestSplitNodesEdgeCases(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    
    def test_no_images(self):
        node = TextNode("This is just plain text.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is just plain text.", TextType.TEXT)],
            new_nodes
        )

    def test_image_at_start(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)text after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("text after", TextType.TEXT),
            ],
            new_nodes
        )

    def test_image_at_end(self):
        node = TextNode("text before![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("text before", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes
        )

    def test_only_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            new_nodes
        )

    def test_consecutive_images(self):
        node = TextNode("![image1](url1)![image2](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "url1"),
                TextNode("image2", TextType.IMAGE, "url2"),
            ],
            new_nodes
        )

    def test_no_links(self):
        node = TextNode("This is just plain text.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is just plain text.", TextType.TEXT)],
            new_nodes
        )

    def test_link_at_start(self):
        node = TextNode("[link](https://boot.dev)text after", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode("text after", TextType.TEXT),
            ],
            new_nodes
        )

    def test_link_at_end(self):
        node = TextNode("text before[link](https://boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("text before", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_only_link(self):
        node = TextNode("[Only a link](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("Only a link", TextType.LINK, "https://www.boot.dev")],
            new_nodes
        )

    def test_consecutive_links(self):
        node = TextNode("[link1](url1)[link2](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "url1"),
                TextNode("link2", TextType.LINK, "url2"),
            ],
            new_nodes
        )