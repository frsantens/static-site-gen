import unittest

from htmlnode import *


class TestTextNode(unittest.TestCase):
 
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_2(self):
        node = LeafNode(None,None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_props_to_html(self):
        testprop = {
            "href": "https://www.google.com",
            "target": "_blank",
            }
        string = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode("node2 tag", props=testprop)
        self.assertEqual(node.props_to_html(), string)

    def test_props_to_html2(self): #test props = None
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')

    def test_not_eq(self):
        node1 = HTMLNode("a")
        node2 = HTMLNode()
        self.assertNotEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()