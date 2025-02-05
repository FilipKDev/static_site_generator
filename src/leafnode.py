from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, children=None, props=None):
        super().__init__(tag, value, children, props)
        self.children = None

    def to_html(self):
        if self.value == None:
            raise ValueError("leaf node must have a value")
        if self.tag == None:
            return self.value
        else:
            html_string = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            return html_string