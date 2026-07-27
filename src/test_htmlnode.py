import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_html_node_init(self):
        node = HTMLNode(
            tag="div",
            value="Hello",
            children=[],
            props={"class": "container"},
        )

        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "container"})

    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://google.com",
                "target": "_blank",
            }
        )

        result = node.props_to_html()

        self.assertEqual(result, ' href="https://google.com" target="_blank" ')

    def test_props_to_html_empty(self):
        node = HTMLNode()

        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")


if __name__ == "__main__":
    unittest.main()
