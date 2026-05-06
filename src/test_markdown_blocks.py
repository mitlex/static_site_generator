import unittest

from markdown_blocks import *

class TestMarkdownBlock(unittest.TestCase):
    #-------------markdown_to_blocks function Tests-------------
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines_odd(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines_even(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_images_and_links(self):
        md = """
This is **bolded** paragraph with an ![image](url)

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line with a [link](url)

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph with an ![image](url)",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line with a [link](url)",
                "- This is a list\n- with items",
            ],
        )

#-------------block_to_block_type function Tests-------------
    def test_block_to_block_type_paragraph(self):
            block = """This is **bolded** paragraph"""
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.PARAGRAPH
            )

    def test_block_to_block_type_heading(self):
            block = """# This is a heading"""
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.HEADING
            )

    def test_block_to_block_type_heading_six(self):
            block = """###### This is a heading"""
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.HEADING
            )

    def test_block_to_block_type_heading_seven(self):
            block = """####### This is NOT a heading"""
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.PARAGRAPH
            )

    def test_block_to_block_type_heading_no_space(self):
            block = """#This is NOT a heading"""
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.PARAGRAPH
            )
    
    def test_block_to_block_type_code(self):
            block = """```
This is code```"""
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.CODE
            )

    def test_block_to_block_type_code_no_new_line(self):
            block = """```This is NOT code```"""
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.PARAGRAPH
            )

    def test_block_to_block_type_code_no_end(self):
            block = """```
This is NOT code"""
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.PARAGRAPH
            )
    
    def test_block_to_block_type_code_no_start(self):
            block = """
This is NOT code```"""
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.PARAGRAPH
            )

    def test_block_to_block_type_quote_with_space(self):
            block = """> this is a quote block
> this is the second line in a quote block"""
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.QUOTE
            )
    
    def test_block_to_block_type_quote_without_space(self):
            block = """>this is a quote block
>this is the second line in a quote block"""
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.QUOTE
            )
    
    def test_block_to_block_type_not_quote(self):
            block = """>this is NOT a quote block
because this line doesn't start with >"""
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.PARAGRAPH
            )

    def test_block_to_block_type_unordered_list(self):
            block = """- this is an unordered list item
- this is another unordered list item"""
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.UNORDERED_LIST
            )

    def test_block_to_block_type_not_unordered_list(self):
            block = """-this is NOT an unordered list
-because we didn't use a space after -"""
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.PARAGRAPH
            )

    def test_block_to_block_type_not_unordered_list_missing_hyphen(self):
            block = """- this is NOT an unordered list
because this is line is missing a hyphen (-)"""
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.PARAGRAPH
            )

    def test_block_to_block_type_ordered_list(self):
            block = """1. this is an ordered list item
2. this is another ordered list item"""
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.ORDERED_LIST
            )

    def test_block_to_block_type_not_ordered_list_wrong_numbers(self):
            block = """2. this is NOT an ordered list
3. because the list does not start with 1. """
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.PARAGRAPH
            )

    def test_block_to_block_type_not_ordered_list_wrong_incrementation(self):
            block = """1. this is NOT an ordered list
3. because this list item does not start with 2. """
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.PARAGRAPH
            )

    def test_block_to_block_type_not_ordered_list_no_space_after_1(self):
            block = """1.this is NOT an ordered list
2. because the first line didn't include a space after 1."""
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type,
                BlockType.PARAGRAPH
            )

    #-------------markdown_to_html_node function Tests-------------
    def test_markdown_to_html_node_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_markdown_to_html_node_heading_1(self):
            md = """
# this is a heading
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><h1>this is a heading</h1></div>",
            )

    def test_markdown_to_html_node_heading_6(self):
            md = """
###### this is a heading
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><h6>this is a heading</h6></div>",
            )

    def test_markdown_to_html_node_blockquote(self):
            md = """
> this is a quote
> that is
> a cool quote
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><blockquote>this is a quote that is a cool quote</blockquote></div>",
            )

    def test_markdown_to_html_node_ulist(self):
            md = """
- this is an unordered list
- with
- 3 list items
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ul><li>this is an unordered list</li><li>with</li><li>3 list items</li></ul></div>",
            )

    def test_markdown_to_html_node_olist(self):
            md = """
1. this is an ordered list
2. with
3. 3 list items
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ol><li>this is an ordered list</li><li>with</li><li>3 list items</li></ol></div>",
            )

    def test_markdown_to_html_node_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_to_html_node_paragraph_and_heading(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

# this is a heading
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><h1>this is a heading</h1></div>",
        )
    
    def test_markdown_to_html_node_quote_then_uolist(self):
        md = """
> This is a quote
> with
> 3 lines

- this is an unordered list
- with
- 3 lines
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with 3 lines</blockquote><ul><li>this is an unordered list</li><li>with</li><li>3 lines</li></ul></div>",
        )

    def test_markdown_to_html_node_heading_quote_paragraph(self):
        md = """
# This is a heading

> This is a quote
> with 2 lines

This is a **bold** paragraph
with _italics_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><blockquote>This is a quote with 2 lines</blockquote><p>This is a <b>bold</b> paragraph with <i>italics</i></p></div>",
        )

    def test_markdown_to_html_node_olist_bold_italic(self):
            md = """
1. this is an ordered list
2. with
3. **3** _list_ items
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><ol><li>this is an ordered list</li><li>with</li><li><b>3</b> <i>list</i> items</li></ol></div>",
            )

if __name__ == "__main__":
    unittest.main()