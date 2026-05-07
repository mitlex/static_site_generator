class HTMLNode:
    """Represents a node in an HTML document tree.

    A node can represent a specific HTML tag and its associated data, such as 
    child nodes, text value, and attributes. It is designed to be a base class 
    for more specialized nodes.

    Attributes:
        tag (str, optional): The HTML tag name (e.g., "p", "a"). If None, 
            the node represents raw text.
        value (str, optional): The text content within the tag. If None, 
            it is assumed the node has children.
        children (list, optional): A list of HTMLNode objects representing 
            the children of this node.
        props (dict, optional): A dictionary of attributes for the tag 
            (e.g., {"href": "url"}).
    """
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value 
        self.children = children 
        self.props = props 

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        """Converts the properties dictionary to an HTML attribute string.

        Each key-value pair in the props dictionary is formatted as 
        key="value" and prefixed with a leading space.

        Returns:
            str: A formatted string of HTML attributes. Returns an empty 
                string if there are no properties.
        """
        if self.props == None or self.props == {}:
            return ""
        html_str = ""
        for k,v in self.props.items():
            html_str += " " f'{k}="{v}"' #HTML attributes are always separated by spaces
        return html_str

    def __repr__(self):
        """Returns a string representation of the HTMLNode object."""
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    """A node that represents a single HTML tag without child nodes.

    A LeafNode is a 'leaf' in the tree, meaning it contains a value (text) 
    but no nested nodes.

    Attributes:
        tag (str): The HTML tag name.
        value (str): The text content of the tag.
        props (dict, optional): Dictionary of HTML attributes.
    """
    def __init__(self, tag, value, props=None):
        """Initializes a LeafNode with tag, value, and properties."""
        super().__init__(tag, value, None, props)

    def to_html(self):
        """Renders the node as an HTML string.

        Returns:
            str: The rendered HTML tag including its value and properties.
                If no tag is present, returns the raw value.

        Raises:
            ValueError: If the value attribute is None.
        """
        if self.value is None:
            raise ValueError("all LeafNode objects must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        """Returns a string representation of the LeafNode object."""
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    """A node that represents an HTML tag containing other nodes.

    ParentNodes handle the nesting of HTML elements. They do not have 
    a direct value; instead, they contain a list of children which 
    can be either LeafNodes or other ParentNodes.

    Attributes:
        tag (str): The HTML tag name.
        children (list): A list of HTMLNode objects representing the 
            nested content.
        props (dict, optional): Dictionary of HTML attributes.
    """
    def __init__(self, tag, children, props=None):
        """Initializes a ParentNode with tag, children, and properties."""
        super().__init__(tag, None, children, props)

    def to_html(self):
        """Recursively renders the node and its children as an HTML string.

        Returns:
            str: The rendered HTML string including the opening tag, 
                all rendered children, and the closing tag.

        Raises:
            ValueError: If the tag is None or if the children list is None.
        """
        if self.tag is None:
            raise ValueError("all ParentNode objects must have a tag")
        if self.children is None:
            raise ValueError("all ParentNode objects must have atleast one child node")
        child_str = ""
        for child in self.children:
            child_str += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_str}</{self.tag}>"
