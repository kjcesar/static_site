class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError(
            "Child classes will override this method to render themselves as HTML."
        )

    def props_to_html(self):
        """It should return a formatted string representing the HTML attributes of the node. For example, if self.props is:

        {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        Then self.props_to_html() should return:

         href="https://www.google.com" target='_blank'
        """
        if self.props is None:
            return ""
        string_to_return = " "
        for attribute_name, attribute_value in self.props.items():
            string_to_return += attribute_name + "=" + '"' + attribute_value + '"' + " "

        return string_to_return

    def __repr__(self) -> str:
        sentence1 = f"HTMLNode object with tag {self.tag}, value {self.value}, children{self.children}"
        sentence2 = f"and props {self.props}"

        return f"{sentence1} \n {sentence2}"


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str | None, props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")

        if self.tag is None:
            return self.value

        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        sentence1 = f"HTMLNode object with tag {self.tag}, value {self.value}"
        sentence2 = f"and props {self.props}"

        return f"{sentence1} \n {sentence2}"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        children: list["HTMLNode"] | None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing Tag")
        if self.children is None:
            raise ValueError("Missing Child")

        else:
            web = f"<{self.tag}>"
            web2 = ""
            for child in self.children:
                web2 += child.to_html()
            web3 = f"</{self.tag}>"
            return web + web2 + web3
