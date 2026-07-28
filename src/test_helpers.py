import unittest
from textnode import TextNode, TextType
from helpers import text_node_to_html_node, split_nodes_delimiter


class TestHelpers(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        # new_nodes should be a list with these text nodes
        list_old = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(list_old, new_nodes)

    def test_split_nodes_delimiter2(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.CODE)
        # new_nodes should be a list with these text nodes
        list_old = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(list_old, new_nodes)
