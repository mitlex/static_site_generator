from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Splits text-type nodes into multiple nodes based on a markdown delimiter.

    Iterates through a list of nodes and identifies text nodes containing the
    specified delimiter. It splits the content, alternating between regular 
    text and the new text_type. Non-text nodes are preserved as-is.

    Args:
        old_nodes (list): A list of TextNode objects.
        delimiter (str): The markdown character(s) to split by (e.g., "**", "`").
        text_type (TextType): The type to assign to the delimited text.

    Returns:
        list: A new list of TextNode objects with the split content.

    Raises:
        Exception: If a closing delimiter is not found (odd number of parts).
    """
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

def split_nodes_link(old_nodes):
    """Splits text nodes into multiple nodes by extracting markdown links.

    Processes a list of nodes and identifies markdown link syntax: [anchor](url).
    Text nodes containing links are broken into regular text nodes and link nodes.
    Non-text nodes are appended to the new list unchanged.

    Args:
        old_nodes (list): A list of TextNode objects to process.

    Returns:
        list: A new list of TextNode objects where links have been isolated.
    """
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

def split_nodes_image(old_nodes):
    """Splits text nodes into multiple nodes by extracting markdown images.

    Processes a list of nodes and identifies markdown image syntax: ![alt text](url).
    Text nodes containing images are broken into regular text nodes and image nodes.
    Non-text nodes are preserved in the list.

    Args:
        old_nodes (list): A list of TextNode objects to process.

    Returns:
        list: A new list of TextNode objects where images have been isolated.
    """
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

def text_to_textnodes(text):
    """Converts a raw markdown string into a list of specialized TextNodes.

    This function applies a sequence of splitting rules to process inline 
    markdown syntax including bold, italic, code blocks, images, and links.

    Args:
        text (str): The raw markdown string to be parsed.

    Returns:
        list: A list of TextNode objects representing the parsed content.
    """
    nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def extract_markdown_links(text):
    """Extracts markdown link components from a string using regex.

    Identifies standard markdown links while explicitly ignoring image 
    syntax by using a negative lookbehind for the '!' character.

    Args:
        text (str): The raw markdown string to search.

    Returns:
        list of tuple: A list of tuples, where each tuple contains 
            (anchor_text, url).
    """
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_images(text):
    """Extracts markdown image components from a string using regex.

    Identifies markdown image syntax specifically by looking for the leading
    '!' followed by brackets and parentheses.

    Args:
        text (str): The raw markdown string to search.

    Returns:
        list of tuple: A list of tuples, where each tuple contains 
            (alt_text, url).
    """
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


