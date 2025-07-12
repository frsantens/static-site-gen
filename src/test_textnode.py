# The above class contains unit tests for classes related to text and HTML nodes, including tests for
# equality, splitting nodes based on a delimiter, and converting a text node to an HTML node.
import unittest

from textnode import *
from htmlnode import *
from split_node import split_nodes_delimiter
from main import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_not_eq1(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD, "http...com")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_link_None(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_link_None2(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, "http...com")
        self.assertNotEqual(node, node2)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_split(self):
        old = [TextNode("_hello_world", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old, "_", TextType.ITALIC)

    def test_no_split_for_different_type(self):
        old = [TextNode("*hello,world*", TextType.BOLD)]
        expected = [
            TextNode("",text_type = TextType.TEXT),
            TextNode("hello,world", TextType.BOLD),
            TextNode("",text_type = TextType.TEXT),
            ]
        self.assertEqual(split_nodes_delimiter(old, "*", TextType.TEXT), expected)

    def test_multiple_nodes(self):
        old = [
            TextNode("a,b", TextType.TEXT),
            TextNode("c", TextType.BOLD),
            TextNode(f"d,e,  'f' olala", TextType.TEXT),
        ]
        expected = [
            TextNode("a,b", TextType.TEXT),
            TextNode("c", TextType.BOLD),
            TextNode("d,e,  ", TextType.TEXT),
            TextNode("f", TextType.CODE),
            TextNode(" olala", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(old, "`", TextType.CODE), expected)

    def test_leading_and_trailing_delimiters(self):
        old = [TextNode("*start,end*", TextType.TEXT)]
        expected = [
            TextNode("start,end", TextType.BOLD),
        ]
        self.assertEqual(split_nodes_delimiter(old, "*", TextType.BOLD), expected)

    def test_no_delimiter(self):
        old = [TextNode("hello world", TextType.TEXT)]
        expected = [TextNode("hello world", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(old, "*", TextType.BOLD), expected)


if __name__ == "__main__":
    unittest.main()