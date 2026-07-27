from textnode import TextNode, TextType


def main():
    something = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(something)


main()
