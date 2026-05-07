from enum import Enum

from htmlnode import *

class TextType(Enum):
    """Supported types of inline text nodes.

    Attributes:
        TEXT: Plain text without formatting.
        BOLD: Bolded text.
        ITALIC: Italicized text.
        CODE: Inline code snippets.
        LINK: Hyperlink with a URL.
        IMAGE: Image with a source URL and alt text.
    """
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    """Represents a piece of inline text and its associated formatting.

    Attributes:
        text (str): The raw text content of the node.
        text_type (TextType): The type of formatting to apply.
        url (str, optional): The URL for links or images. Defaults to None.
    """
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        """Checks if two TextNodes are identical in content and type."""
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        """Returns a string representation of the TextNode."""
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    """Converts a TextNode into a LeafNode for HTML rendering.

    Args:
        text_node (TextNode): The inline text node to be converted.

    Returns:
        LeafNode: A leaf node object ready for conversion to an HTML string.

    Raises:
        Exception: If the text_node.text_type is not a member of the TextType enum.
    """
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, props={"href": f"{text_node.url}"})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", props={"src": f"{text_node.url}", "alt": f"{text_node.text}"})
    else:
        raise Exception("Error: TextType is not [TEXT, BOLD, ITALIC, CODE, LINK, IMAGE]")