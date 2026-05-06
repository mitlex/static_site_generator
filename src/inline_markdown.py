from textnode import *
import re

"""
split_nodes_delimiter function allows us to create TextNodes from raw Markdown strings.

inputs:
old_nodes = list of TextNodes
delimiter (e.g. ` is the code delimiter in markdown, ** for bold, _ for italic)
text type (e.g. TextType.CODE, matching the delimiter)

returns:
new list of TextNodes, where any "text" type nodes in the input list are potentially split into multiple TextNodes based on the syntax.

e.g.

node = TextNode("This is text with a `code block` word", TextType.TEXT)
new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

new_nodes becomes:

[
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
]

Note: for simplicity, this function will not handle nested inline text types (e.g. "This is an _italic and **bold** word_.")
Note: this function does handle cases like "hello **my name is** Bob and **I am a bold person**"

Note: to handle blocks of text containing multiple delimiters:

e.g. ("hello `this is code` and **this is bold**!")

You need to chain function calls like so:

node = TextNode("hello `this is code` and **this is bold**!", TextType.TEXT)
nodes = split_nodes_delimiter([node], "`", TextType.CODE) # First pass: handle code
nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD) # Second pass, handle bold
"""
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            split_text = old_node.text.split(delimiter)
            if len(split_text)%2 == 0:
                raise Exception(f"delimiter {delimiter} not closed, invalid markdown")
            else:
                for i, part in enumerate(split_text):
                    if part == "": #skip empty strings so we don't create empty TextNodes
                        continue
                    if i%2 == 0: #even indeces = regular text
                        new_nodes.append(TextNode(part, TextType.TEXT))
                    else: #odd indeces = not regular text
                        new_nodes.append(TextNode(part, text_type))

    return new_nodes

"""
Input: 
list of TextNodes

Returns: 
new list of TextNodes, where any "text" type nodes in the input list are potentially split into multiple TextNodes if a markdown link is contained in the text
"""
def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            md_links = extract_markdown_links(old_node.text)
            if md_links == []:
                if old_node.text != "":
                    new_nodes.append(old_node)
            else:
                remaining_text = old_node.text
                for tup in md_links:
                    delimiter = f"[{tup[0]}]({tup[1]})" #reconstructing markdown as delimiter e.g. [alttext](link)
                    split_on_link_md = remaining_text.split(delimiter, 1)
                    if split_on_link_md[0] != "":
                        new_nodes.append(TextNode(split_on_link_md[0], TextType.TEXT))
                    new_nodes.append(TextNode(tup[0], TextType.LINK, tup[1]))
                    remaining_text = split_on_link_md[1]
                if remaining_text != "":
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

"""
Input: 
list of TextNodes

Returns: 
new list of TextNodes, where any "text" type nodes in the input list are potentially split into multiple TextNodes if a markdown image is contained in the text
"""
def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            md_images = extract_markdown_images(old_node.text)
            if md_images == []:
                if old_node.text != "":
                    new_nodes.append(old_node)
            else:
                remaining_text = old_node.text
                for tup in md_images:
                    delimiter = f"![{tup[0]}]({tup[1]})" #reconstructing markdown as delimiter e.g. ![image](link)
                    split_on_image_md = remaining_text.split(delimiter, 1)
                    if split_on_image_md[0] != "":
                        new_nodes.append(TextNode(split_on_image_md[0], TextType.TEXT))
                    new_nodes.append(TextNode(tup[0], TextType.IMAGE, tup[1]))
                    remaining_text = split_on_image_md[1]
                if remaining_text != "":
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

"""
Input: raw markdown text

Returns: a list of TextNodes
"""
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

"""
Input: raw markdown text

Returns: List of tuples (anchor text, URL) of markdown links contained within input text
"""
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

"""
Input: raw markdown text

Returns: List of tuples (alttext, URL) of markdown images contained within input text
"""
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


