#"HTMLNode" class will represent a "node" in an HTML document tree (like a <p> tag and its contents, 
# or an <a> tag and its contents). It can be block level or inline, and is designed to only output HTML.

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag #string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value #string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children #list of HTMLNode objects representing the children of this node
        self.props = props #dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "link"}

        #why all attributes = None by default?
        #An HTMLNode without a tag will just render as raw text
        #An HTMLNode without a value will be assumed to have children
        #An HTMLNode without children will be assumed to have a value
        #An HTMLNode without props simply won't have any attributes

    def to_html(self):
        raise NotImplementedError
    
    """
    props_to_html
    return a formatted string representing the HTML attributes of the node
    e.g. 
    if self.props is:
    {
        "href": "link",
        "target": "_blank",
    }
    this method will return:
    href="link" target="_blank"
    """
    def props_to_html(self):
        if self.props == None or self.props == {}:
            return ""
        html_str = ""
        for k,v in self.props.items():
            html_str += " " f'{k}="{v}"' #HTML attributes are always separated by spaces
        return html_str

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

"""
A LeafNode is a type of HTMLNode that represents a single HTML tag with no children. For example, a simple <p> tag with some text inside of it:

<p>This is a paragraph of text.</p>

We call it a "leaf" node because it's a "leaf" in the tree of HTML nodes. It's a node with no children. In this next example, <p> is not a leaf node, but <b> is.

<p>
  This is a paragraph. It can have a lot of text inside.
  <b>This is bold text.</b>
  This is the last sentence.
</p>
"""
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("all LeafNode objects must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
"""
The ParentNode class will handle the nesting of HTML nodes inside of one another. 

Any HTML node that's not a "leaf" node (i.e. it has children) is a "parent" node.
"""
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("all ParentNode objects must have a tag")
        if self.children is None:
            raise ValueError("all ParentNode objects must have atleast one child node")
        child_str = ""
        for child in self.children:
            child_str += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_str}</{self.tag}>"
