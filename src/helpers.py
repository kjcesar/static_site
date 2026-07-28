from textnode import TextType, TextNode
from htmlnode import LeafNode


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("link", text_node.text)

    else:
        raise ValueError(f"Unknown text type: {text_node.text_type}")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_list.append(old_node)
        elif delimiter not in old_node.text:
            raise Exception(
                f"delimiter not in node: {old_node} invalid Markdown Syntax"
            )
        else:
            texts = old_node.text.split(delimiter)
            if len(texts) % 2 == 0:
                # cause markdown allways will split uneven
                raise Exception("invalid Markdown syntax")
            for index, text in enumerate(texts):
                if index % 2 != 0:
                    new_list.append(TextNode(text, text_type))
                else:
                    new_list.append(TextNode(text, TextType.TEXT))

    return new_list
