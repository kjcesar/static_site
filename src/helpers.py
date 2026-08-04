from textnode import TextType, TextNode
from htmlnode import LeafNode
import re


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


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r" \[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list = []
    for old_node in old_nodes:
        text = old_node.text
        if old_node.text_type != TextType.TEXT:  # it is not text?
            new_list.append(old_node)
            continue

        images = extract_markdown_images(text)
        if not images or not text:
            new_list.append(old_node)
        else:
            for img in images:
                separator = f"![{img[0]}]({img[1]})"
                before, after = text.split(separator, 1)
                # what if before is empty, i dont want TextNode("")
                text = after
                if before:
                    new_list.append(TextNode(before, TextType.TEXT))
                new_list.append(TextNode(img[0], TextType.IMAGE, img[1]))
            if text:
                new_list.append(TextNode(text, TextType.TEXT))

    return new_list


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list = []
    for old_node in old_nodes:
        text = old_node.text
        if old_node.text_type != TextType.TEXT:  # it is not text?
            new_list.append(old_node)
            continue

        links = extract_markdown_links(text)
        if not links or not text:
            new_list.append(old_node)
        else:
            for link in links:
                separator = f"[{link[0]}]({link[1]})"
                before, after = text.split(separator, 1)
                # what if before is empty, i dont want TextNode("")
                text = after
                if before:
                    new_list.append(TextNode(before, TextType.TEXT))
                new_list.append(TextNode(link[0], TextType.LINK, link[1]))
            if text:
                new_list.append(TextNode(text, TextType.TEXT))

    return new_list
