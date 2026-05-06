import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    #-------------props_to_html Tests-------------

    def test_props_to_html_basic(self):
        child1 = HTMLNode()
        child2 = HTMLNode()
        node = HTMLNode("a", "hello", [child1, child2], {"href": "link", "target": "_blank"})
        self.assertEqual(' href="link" target="_blank"', node.props_to_html())

    def test_props_to_html_one_attribute(self):
        child1 = HTMLNode()
        child2 = HTMLNode()
        node = HTMLNode("a", "hello", [child1, child2], {"href": "link"})
        self.assertEqual(' href="link"', node.props_to_html())

    def test_props_to_html_props_only(self):
        child1 = HTMLNode()
        child2 = HTMLNode()
        node = HTMLNode(props={"href": "link"})
        self.assertEqual(' href="link"', node.props_to_html())

    def test_props_none(self):
        node = HTMLNode("a", "hello", props=None)
        self.assertEqual("", node.props_to_html())

    def test_props_empty(self):
        node = HTMLNode("a", "hello", props={})
        self.assertEqual("", node.props_to_html())

    #-------------LeafNode Tests-------------

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_props(self):
        node = LeafNode("a", "check out my link!", props={"href": "link"})
        self.assertEqual(node.to_html(), '<a href="link">check out my link!</a>')

    def test_leaf_to_html_value_none(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "just a bunch of text")
        self.assertEqual(node.to_html(), "just a bunch of text")

    #-------------ParentNode Tests-------------

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_without_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_without_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_greatgrandchildren(self):
        greatgrandchild_node = LeafNode("b", "greatgrandchild")
        grandchild_node = ParentNode("span", [greatgrandchild_node])
        child_node = ParentNode("div", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><div><span><b>greatgrandchild</b></span></div></div>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(parent_node.to_html(),'<div class="container"><span>child</span></div>')

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(),"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

if __name__ == "__main__":
    unittest.main()