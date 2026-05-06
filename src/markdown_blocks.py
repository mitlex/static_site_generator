from enum import Enum

from htmlnode import *
from inline_markdown import *
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

"""
Input: single block of markdown text

Returns: the BlockType representing the type of block it is
"""
def block_to_block_type(block):
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


"""
Input: raw markdown string (representing a full document)

Returns: list of "block" strings

---Example---

Input:
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

Returns:
[
    "This is **bolded** paragraph",
    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
    "- This is a list\n- with items",
]
"""
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        if block == "":
            continue
        else:
            new_blocks.append(block.strip())
    return new_blocks

"""
Input: markdown text 

Returns: parent html_node representing the entire document of markdown text, with appropriately nested child nodes
"""
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_html_node(block))
    return ParentNode("div", children)

"""
Helper function that checks block type and returns the appropriate function which converts that block to an htmlnode.
Input: block of markdown text
Returns: function that converts block to htmlnode
"""
def block_to_html_node(block):
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
    
"""
Helper function for block_to_html_node
"""
def paragraph_to_html_node(block):
    paragraph_remove_newlines = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(paragraph_remove_newlines))

"""
Helper function for block_to_html_node
"""
def heading_to_html_node(block):
    leading_hash_count = len(block) - len(block.lstrip("#"))
    text = block[leading_hash_count+1:] #+1 accounts for space between #'s and text 
    return ParentNode(f"h{leading_hash_count}", text_to_children(text))

"""
Helper function for block_to_html_node
"""
def quote_to_html_node(block):
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

"""
Helper function for block_to_html_node

We don't use text_to_children function here because the code block shouldn't do any inline markdown parsing of its children. This keeps the text in the code block as is.
"""
def code_to_html_node(block):
    text = block[4:-3] #remove first ``` and newline, and last ```
    text_node = TextNode(text, TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [html_node])
    return ParentNode("pre", [code_node])

"""
Helper function for block_to_html_node
"""
def ulist_to_html_node(block):
    lines = block.split("\n")
    list_nodes = []
    for line in lines:
        list_nodes.append(ParentNode("li", text_to_children(line[2:]))) #line[2:] strips starting "- "
    return ParentNode("ul", list_nodes)

"""
Helper function for block_to_html_node
"""
def olist_to_html_node(block):
    lines = block.split("\n")
    list_nodes = []
    for line in lines:
        list_nodes.append(ParentNode("li", text_to_children(line.split(". ", maxsplit=1)[1]))) #line.split(". ", maxsplit=1)[1] strips starting "X. " where X is any integer.
    return ParentNode("ol", list_nodes)

"""
Helper function for *_to_html_node helper functions

Input: markdown text

Returns: a list of HTMLNode's representing inline markdown 

Note: convert text to textnodes, then textnodes to htmlnodes using text_node_to_html_node function
"""
def text_to_children(text):
    return list(map(text_node_to_html_node, text_to_textnodes(text)))