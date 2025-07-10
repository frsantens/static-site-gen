import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
 

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