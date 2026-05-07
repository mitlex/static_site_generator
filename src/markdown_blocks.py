from enum import Enum

from htmlnode import *
from inline_markdown import *
from textnode import text_node_to_html_node

class BlockType(Enum):
    """Enumeration of supported Markdown block types.

    Defines the different types of structural blocks that can be identified 
    within a markdown document.
    """
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    """Determines the type of a markdown block based on its syntax.

    Analyzes the prefix and structure of a single block of markdown text 
    to categorize it as a heading, code block, quote, list, or paragraph.

    Args:
        block (str): A single block of markdown text.

    Returns:
        BlockType: The corresponding BlockType enumeration value.
    """
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    elif (block.startswith("```\n") and block.endswith("```")):
        return BlockType.CODE
    
    elif block.startswith(("> ", ">")):
        lines = block.split("\n")
        for line in lines:
            if line.startswith(("> ", ">")):
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    elif block.startswith("- "):
        lines = block.split("\n")
        for line in lines:
            if line.startswith("- "):
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    elif block.startswith("1. "):
        lines = block.split("\n")

        i = 1
        for line in lines:
            if line.startswith(f"{i}. "):
                i+=1
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    
    else:
        return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    """Splits a full markdown document into a list of block strings.

    Blocks are identified by being separated by one or more empty lines. 
    Each block is stripped of leading and trailing whitespace, and 
    empty blocks are discarded.

    Args:
        markdown (str): The raw markdown document text.

    Returns:
        list: A list of strings, where each string is a single structural 
            block (e.g., a paragraph, list, or heading).
    """
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        if block == "":
            continue
        else:
            new_blocks.append(block.strip())
    return new_blocks

def markdown_to_html_node(markdown):
    """Converts a full markdown document into a single parent HTMLNode.

    The document is first split into blocks, and each block is converted 
    into its respective HTMLNode structure. The final output is wrapped 
    in a 'div' tag as the root container.

    Args:
        markdown (str): The raw markdown document text.

    Returns:
        ParentNode: A 'div' ParentNode containing the entire nested 
            structure of the document as children.
    """
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_html_node(block))
    return ParentNode("div", children)

def block_to_html_node(block):
    """Converts a markdown block into its corresponding HTMLNode structure.

    This function identifies the BlockType of the input and delegates the 
    actual HTML conversion to the specialized helper function for that type.

    Args:
        block (str): A single block of markdown text.

    Returns:
        HTMLNode: An HTMLNode (or subclass) representing the block and its 
            parsed inline content.
    """
    block_type = block_to_block_type(block) #use block_type to determine tag

    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)

def paragraph_to_html_node(block):
    """Converts a markdown paragraph block into a paragraph HTMLNode.

    Joins multi-line paragraph text into a single line and parses any 
    inline markdown syntax within the text.

    Args:
        block (str): The raw markdown paragraph text.

    Returns:
        ParentNode: A 'p' tag ParentNode containing the parsed inline 
            content as child nodes.
    """
    paragraph_remove_newlines = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(paragraph_remove_newlines))

def heading_to_html_node(block):
    """
    Converts a markdown heading block into an HTML ParentNode.

    Args:
        block (str): A string representing a markdown heading block 
            (e.g., "### This is a heading").

    Returns:
        ParentNode: An HTML node representing the appropriate 
            heading level (h1-h6) with nested inline children.
    """
    leading_hash_count = len(block) - len(block.lstrip("#"))
    text = block[leading_hash_count+1:] #+1 accounts for space between #'s and text 
    return ParentNode(f"h{leading_hash_count}", text_to_children(text))

def quote_to_html_node(block):
    """
    Converts a markdown blockquote into an HTML blockquote ParentNode.

    Args:
        block (str): A multi-line string where each line begins with a 
            '>' character.

    Returns:
        ParentNode: A 'blockquote' HTML node containing the processed 
            text as child nodes.
    """
    lines = block.split("\n")
    stripped = []
    for line in lines:
        # Strip exactly one ">" and one optional space (not lstrip("> "),
        # which would greedily eat all leading ">" and spaces, mangling
        # nested quotes like "> > nested" into "nested").
        if line.startswith(">"):
            line = line[1:]
            if line.startswith(" "):
                line = line[1:]
        stripped.append(line)
    text = " ".join(stripped)
    return ParentNode("blockquote", text_to_children(text))

def code_to_html_node(block):
    """
    Converts a markdown code block into a nested pre/code HTML structure.

    This function specifically avoids using 'text_to_children' to ensure that 
    the content within the code block is not parsed for inline markdown, 
    preserving the literal text.

    Args:
        block (str): A string starting and ending with triple backticks (```).

    Returns:
        ParentNode: A 'pre' node containing a 'code' child node which 
            holds the raw text.
    """
    text = block[4:-3] #remove first ``` and newline, and last ```
    text_node = TextNode(text, TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [html_node])
    return ParentNode("pre", [code_node])

def ulist_to_html_node(block):
    """
    Converts a markdown unordered list block into an HTML 'ul' ParentNode.

    Args:
        block (str): A string containing multiple lines, where each line 
            starts with a '-' followed by a space.

    Returns:
        ParentNode: A 'ul' ParentNode containing a list of 'li' ParentNodes, 
            each containing the parsed inline elements of a list item.
    """
    lines = block.split("\n")
    list_nodes = []
    for line in lines:
        list_nodes.append(ParentNode("li", text_to_children(line[2:]))) #line[2:] strips starting "- "
    return ParentNode("ul", list_nodes)

def olist_to_html_node(block):
    """
    Converts a markdown ordered list block into an HTML 'ol' ParentNode.

    Args:
        block (str): A multi-line string where each line begins with an 
            incrementing number followed by a period and a space (e.g., "1. ").

    Returns:
        ParentNode: An 'ol' node containing a list of 'li' ParentNodes, 
            each containing the parsed inline elements of a list item.
    """
    lines = block.split("\n")
    list_nodes = []
    for line in lines:
        list_nodes.append(ParentNode("li", text_to_children(line.split(". ", maxsplit=1)[1]))) #line.split(". ", maxsplit=1)[1] strips starting "X. " where X is any integer.
    return ParentNode("ol", list_nodes)

def text_to_children(text):
    """
    Converts a raw string of text into a list of HTMLNodes.

    This function processes inline markdown (like bold, italics, and links) 
    by first converting the string into TextNodes and then transforming 
    each TextNode into its corresponding HTMLNode representation.

    Args:
        text (str): The raw markdown text to be parsed.

    Returns:
        list: A list of LeafNode objects representing the inline elements.
    """
    return list(map(text_node_to_html_node, text_to_textnodes(text)))
