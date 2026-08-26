import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)

    def test_different(self):
        node = TextNode("ThIs is a tExt node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text n0de", TextType.IMAGE)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node3, node4)

    def test_url_different(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.yahoo.com")
        self.assertNotEqual(node, node2)

    def test_url_equal(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.google.com")
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
