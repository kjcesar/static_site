import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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

        self.assertEqual(result, ' href="https://google.com" target="_blank"')

    def test_props_to_html_empty(self):
        node = HTMLNode()

        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

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

    def test_leaf_none(self):
        node = LeafNode(None, "some_value")
        self.assertEqual("some_value", node.to_html())

    def test_leaf_none_value(self):
        with self.assertRaises(ValueError) as context:
            LeafNode("div", None).to_html()

        self.assertEqual(str(context.exception), "All leaf nodes must have a value.")

    def test_parent_none_tag(self):
        """
        if self.tag is None:
            raise ValueError("Missing Tag")
        if self.children is None:
            raise ValueError("Missing Child")
        """
        child_node = LeafNode("span", "child")
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [child_node]).to_html()

        self.assertEqual(str(context.exception), "Missing Tag")

    def test_parent_none_value(self):
        """
        if self.tag is None:
            raise ValueError("Missing Tag")
        if self.children is None:
            raise ValueError("Missing Child")
        """
        with self.assertRaises(ValueError) as context:
            ParentNode("p", None).to_html()

        self.assertEqual(str(context.exception), "Missing Child")

    def test_leaf_with_props(self):
        node = LeafNode("img", "some_value", props={"src": "url.png"})

        self.assertEqual(
            node.to_html(),
            '<img src="url.png">some_value</img>',
        )


if __name__ == "__main__":
    unittest.main()
