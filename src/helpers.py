import htmlnode
from textnode import TextType, TextNode
from htmlnode import ParentNode
from block import BlockType
from htmlnode import LeafNode
import re

import textnode


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
            new_list.append(old_node)
            # raise Exception(
            #     f"delimiter not in node: {old_node} invalid Markdown Syntax"
            # )
        else:
            texts = old_node.text.split(delimiter)
            if len(texts) % 2 == 0:
                # cause markdown allways will split uneven
                raise Exception("invalid Markdown syntax")
            for index, text in enumerate(texts):
                if index % 2 != 0:
                    new_list.append(TextNode(text, text_type))
                else:
                    if text != "":
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


def text_to_textnodes(text: str) -> list[TextNode]:
    lista = [TextNode(text, TextType.TEXT)]
    lista = split_nodes_image(lista)
    lista = split_nodes_link(lista)
    lista = split_nodes_delimiter(lista, "**", TextType.BOLD)
    lista = split_nodes_delimiter(lista, "`", TextType.CODE)
    lista = split_nodes_delimiter(lista, "_", TextType.ITALIC)

    return lista


def markdown_to_blocks(markdown):
    parts = markdown.split("\n\n")
    striped_parts = [x.strip() for x in parts if x != ""]

    for index, part in enumerate(striped_parts):
        buffer = []
        if "\n" in part:
            buffer = part.split("\n")
            buffer = [x.strip() for x in buffer]
            striped_parts[index] = "\n".join(buffer)
    for striped_part in striped_parts:
        if striped_part == "":
            striped_parts.pop()
    return striped_parts


## block functions ##
def is_heading(block) -> dict[str, bool | int]:
    """return if is heading and number of #"""
    turnable = {"is_heading": False, "number_of_#": 0}
    found_space = False
    found_text_after_space = False
    if block.startswith("#"):
        for c in block:
            if c == "#":
                turnable["number_of_#"] += 1
            if c == " ":
                found_space = True
                continue  # to check if there is heading text
            elif found_space and c != " ":
                found_text_after_space = True
                break
            else:
                break

        if turnable["number_of_#"] < 7 and found_text_after_space:
            turnable["is_heading"] = True
        return turnable
    else:
        return turnable


def is_code(block):
    if block.startswith("```\n") and block.endswith("```"):
        return True
    else:
        return False


def is_quote(block):
    if block.startswith(">") and block.endswith("<"):
        return True
    else:
        return False


def is_ordered_list(block):
    if not block.startswith("1. "):
        return False

    number = 1
    for line in block.split("\n"):
        if line.startswith(f"{number}. "):
            number += 1
            continue
        else:
            return False
    return True


def is_unordered_list(block):
    for line in block.split("\n"):
        if line.startswith("- "):
            return True
        else:
            return False


## end of blocks functions


def block_to_blocktype(block):
    """determine the type of each block"""
    if is_heading(block)["is_heading"]:
        return BlockType.HEADING

    if is_code(block):
        return BlockType.CODE

    if is_quote(block):
        return BlockType.QUOTE

    if is_ordered_list(block):
        return BlockType.ORDERED_LIST

    if is_unordered_list(block):
        return BlockType.UNORDERED_LIST

    return BlockType.PARAGRAPH


def block_to_tag(type: BlockType, heading_level: int | None = None) -> str:
    """return a tag for each block_type"""
    if type == BlockType.HEADING:
        return f"h{heading_level}"

    if type == BlockType.CODE:
        return "pre"
    if type == BlockType.QUOTE:
        return "blockquote"
    if type == BlockType.ORDERED_LIST:
        return "ol"
    if type == BlockType.UNORDERED_LIST:
        return "ul"
    if type == BlockType.PARAGRAPH:
        return "p"


def markdown_to_html_node(markdown) -> ParentNode:
    """
    converts a full markdown document into a single parent HTMLNode
    """
    """
    TODO:
        markdown
        ↓
        markdown_to_blocks()
        ↓
        block
        ↓
        block_to_blocktype()
        ↓
        block-specific handling
        ↓
        text_to_textnodes()
        ↓
        text_node_to_html_node()
        ↓
        HTML tree


        I'd suggest this order:

        Paragraph
        Heading
        Code
        Quote
        Unordered list
        Ordered list

        And for each one, ask yourself:

        What does this block look like as Markdown?

        What should the corresponding HTML structure look like?

        What part is block-level parsing, and what part can I delegate to text_to_textnodes()?
    """
    blocks = markdown_to_blocks(markdown)
    # crear ParentNode Exterior
    super_papa = ParentNode("div", children=[])
    for block in blocks:
        block_type = block_to_blocktype(block)

        if block_type == BlockType.PARAGRAPH:
            # create corresponding html_node
            # ¿qué tienes que hacer para convertir ese block en el ParentNode que representa un <p>?
            # ej> "hello **world**"
            text = block.replace("\n", " ")
            nodes = text_to_textnodes(text)  # devuelve una lista de textNodes
            parent = ParentNode(block_to_tag(block_type), children=[])
            for node in nodes:
                parent.children.append(text_node_to_html_node(node))

            super_papa.children.append(parent)
        elif block_type == BlockType.CODE:
            # TODO: Remove ``` delimiters, preserve internal newlines, create <code> node, wrap in <pre>
            text = block[4:-3]
            parent = ParentNode(
                block_to_tag(block_type), children=[LeafNode("code", text)]
            )

            super_papa.children.append(parent)
        # TODO: Implement QUOTE - remove > markers, handle multiple lines
        # TODO: Implement HEADING - remove # prefix, determine heading level, process inline Markdown
        # TODO: Implement UNORDERED_LIST - process items, create <li> nodes, wrap in <ul>
        # TODO: Implement ORDERED_LIST - process items, create <li> nodes, wrap in <ol>

    return super_papa
