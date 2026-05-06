import unittest

from textnode import *
from inline_markdown import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("link text", TextType.LINK, "link1")
        node2 = TextNode("link text", TextType.LINK, "link1")
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("link text", TextType.LINK, "link1")
        node2 = TextNode("link text", TextType.LINK, "link2")
        self.assertNotEqual(node, node2)

    def test_not_eq_bold_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_bold_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_bold_code(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "link1")
        self.assertEqual(
            "TextNode(This is a text node, bold, link1)", repr(node)
        )

    def test_repr_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(
            "TextNode(This is a text node, bold, None)", repr(node)
        )

    #-------------Convert TextNode to LeafNode Tests-------------
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, url="link")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), '<a href="link">This is a text node</a>')

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, url="link")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), '<img src="link" alt="This is a text node"></img>')

    def test_incorrect_text_type(self):
        node = TextNode("This is a text node", text_type=None)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    #-------------split_nodes_delimiter function Tests-------------
    def test_split_nodes_delimiter_basic(self):
        node = TextNode("This is a **bold** test", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD), 
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" test", TextType.TEXT)
            ])
    
    def test_split_nodes_delimiter_multiple_nodes(self):
        node = TextNode("This is a **bold** test", TextType.TEXT)
        node2 = TextNode("This is a **bold** test", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node, node2], "**", TextType.BOLD), 
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" test", TextType.TEXT),
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" test", TextType.TEXT)
            ])
        
    def test_split_nodes_delimiter_multiple_mixed_node_text_types(self):
        node = TextNode("This is a **bold** test", TextType.TEXT)
        node2 = TextNode("**This is a bold test**", TextType.BOLD)
        self.assertEqual(
            split_nodes_delimiter([node, node2], "**", TextType.BOLD), 
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" test", TextType.TEXT),
                TextNode("**This is a bold test**", TextType.BOLD)
            ])
        
    def test_split_nodes_delimiter_empty_old_nodes_list(self):
        self.assertEqual(
            split_nodes_delimiter([], "**", TextType.BOLD), [])
        
    def test_split_nodes_delimiter_old_node_not_typetext(self):
        node = TextNode("_italics test_", TextType.ITALIC)
        self.assertEqual(
            split_nodes_delimiter([node], "_", TextType.ITALIC), 
            [
                TextNode("_italics test_", TextType.ITALIC),
            ])
        
    def test_split_nodes_delimiter_unclosed_delimiter(self):
        node = TextNode("This is a **bold test", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_nodes_delimiter_two_same_delimiter_one_node(self):
        node = TextNode("This **word** is **bold**!", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD), 
            [
                TextNode("This ", TextType.TEXT),
                TextNode("word", TextType.BOLD),
                TextNode(" is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode("!", TextType.TEXT)
            ])
        
    def test_split_nodes_delimiter_no_delimiter_in_text(self):
        node = TextNode("This is a no delimiter test", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE), 
            [
                TextNode("This is a no delimiter test", TextType.TEXT),
            ])
        
    def test_split_nodes_delimiter_bold_at_start(self):
        node = TextNode("**This** is a no delimiter test", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD), 
            [
                TextNode("This", TextType.BOLD),
                TextNode(" is a no delimiter test", TextType.TEXT),
            ])
        
    def test_split_nodes_delimiter_bold_at_end(self):
        node = TextNode("This is a no delimiter **test**", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD), 
            [
                TextNode("This is a no delimiter ", TextType.TEXT),
                TextNode("test", TextType.BOLD),
            ])
        
    def test_split_nodes_delimiter_only_bold(self):
        node = TextNode("**This is a no delimiter test**", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD), 
            [
                TextNode("This is a no delimiter test", TextType.BOLD),
            ])

    def test_split_nodes_delimiter_code_then_bold(self):
        node = TextNode("hello `this is code` and **this is bold**!", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE) # First pass: handle code
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD) # Second pass, handle bold
        self.assertEqual(
            nodes, 
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("this is code", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("this is bold", TextType.BOLD),
                TextNode("!", TextType.TEXT),
            ])

    #-------------extract_markdown_images function Tests-------------
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](link)"
            )
        self.assertListEqual([("image", "link")], matches)

    def test_extract_markdown_images_rogue_square_brackets(self):
        matches = extract_markdown_images(
            "This is text with an ![im[]age](link)"
            )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_no_exclamation(self):
        matches = extract_markdown_images(
            "This is text with an [image](link)"
            )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![a](one) and ![b](two)"
        )
        self.assertListEqual([("a", "one"), ("b", "two")], matches)

    def test_extract_markdown_images_no_matches(self):
        matches = extract_markdown_images("just plain text")
        self.assertListEqual([], matches)

    #-------------extract_markdown_links function Tests-------------
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](url)"
            )
        self.assertListEqual([("link", "url")], matches)

    def test_extract_markdown_links_rogue_parentheses(self):
        matches = extract_markdown_links(
            "This is text with an [link](ur()l)"
            )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_rogue_exclamation(self):
        matches = extract_markdown_links(
            "This is text with an ![link](url)"
            )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "[a](one) and [b](two)"
        )
        self.assertListEqual([("a", "one"), ("b", "two")], matches)

    def test_extract_markdown_links_no_matches(self):
        matches = extract_markdown_links("just plain text")
        self.assertListEqual([], matches)

    #-------------split_nodes_image function Tests-------------
    def test_split_nodes_image_basic(self):
        node = TextNode(
            "This is text with an ![image](link) and another ![second image](link) one",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "link"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "link"),
                TextNode(" one", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_two_nodes(self):
        node = TextNode(
            "This is text with an ![image](link) in it",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with an ![image](link) in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "link"),
                TextNode(" in it", TextType.TEXT),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "link"),
                TextNode(" in it", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_two_nodes_one_non_text_type(self):
        node = TextNode(
            "This is text with an ![image](link) in it",
            TextType.TEXT,
        )
        node2 = TextNode(
            "**This is bold text**",
            TextType.BOLD,
        )
        new_nodes = split_nodes_image([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "link"),
                TextNode(" in it", TextType.TEXT),
                TextNode("**This is bold text**", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_nodes_image_one_node_plain_text(self):
        node = TextNode(
            "This is text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_image_at_start(self):
        node = TextNode(
            "![image](link) is a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "link"),
                TextNode(" is a link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_no_remaining_text(self):
        node = TextNode(
            "Check out my image: ![image](link)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Check out my image: ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "link"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_empty_list(self):
        new_nodes = split_nodes_image([])
        self.assertListEqual(
            [],
            new_nodes,
        )

    def test_split_nodes_image_empty_text_node(self):
        node = TextNode(
            "",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [],
            new_nodes,
        )

    def test_split_nodes_image_adjacent_images(self):
        node = TextNode(
            "![image](link)![second image](link)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "link"),
                TextNode("second image", TextType.IMAGE, "link"),
            ],
            new_nodes,
        )

    #-------------split_nodes_link function Tests-------------
    def test_split_nodes_link_basic(self):
        node = TextNode(
            "This is text with a [link](url) and another [link](url) one",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" one", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_two_nodes(self):
        node = TextNode(
            "This is text with a [link](url) in it",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with a [link](url) in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" in it", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" in it", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_two_nodes_one_non_text_type(self):
        node = TextNode(
            "This is text with a [link](url) in it",
            TextType.TEXT,
        )
        node2 = TextNode(
            "**This is bold text**",
            TextType.BOLD,
        )
        new_nodes = split_nodes_link([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" in it", TextType.TEXT),
                TextNode("**This is bold text**", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_nodes_link_one_node_plain_text(self):
        node = TextNode(
            "This is text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_link_at_start(self):
        node = TextNode(
            "[link](url) is a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "url"),
                TextNode(" is a link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_link_no_remaining_text(self):
        node = TextNode(
            "Check out my link: [link](url)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out my link: ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_empty_list(self):
        new_nodes = split_nodes_link([])
        self.assertListEqual(
            [],
            new_nodes,
        )

    def test_split_nodes_link_empty_text_node(self):
        node = TextNode(
            "",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [],
            new_nodes,
        )

    def test_split_nodes_link_adjacent_link(self):
        node = TextNode(
            "[link](url)[link](url)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "url"),
                TextNode("link", TextType.LINK, "url"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_pass_image(self):
        node = TextNode(
            "Here is an ![image](img.png) not a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Here is an ![image](img.png) not a link", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_nodes_link_image_and_link(self):
        node = TextNode("look at this ![image](link) and this [link](url)!", TextType.TEXT)
        nodes = split_nodes_image([node]) # First pass: handle image
        nodes = split_nodes_link(nodes) # Second pass, handle link
        self.assertEqual(
            nodes, 
            [
                TextNode("look at this ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "link"),
                TextNode(" and this ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode("!", TextType.TEXT),
            ])

    #-------------text_to_textnodes function Tests-------------
    def test_text_to_textnodes_basic(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![image](url) and a [link](url)")
        self.assertEqual(
            nodes, 
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url")
            ])

    def test_text_to_textnodes_different_order(self):
        nodes = text_to_textnodes("This is _text_ with a **bold** word and a `code block` and an ![image](url) and a [link](url)")
        self.assertEqual(
            nodes, 
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.ITALIC),
                TextNode(" with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url")
            ])

    def test_text_to_textnodes_plain_text(self):
        nodes = text_to_textnodes("This is text")
        self.assertEqual(
            nodes, 
            [
                TextNode("This is text", TextType.TEXT)
            ])
        
    def test_text_to_textnodes_single_type_markdown(self):
        nodes = text_to_textnodes("This is **bold text**")
        self.assertEqual(
            nodes, 
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD)
            ])

if __name__ == "__main__":
    unittest.main()