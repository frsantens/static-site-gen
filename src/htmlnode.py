class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ''
        result = str()
        for k,v in self.props.items():
            result += f' {k}="{v}"'
        return result

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
            super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        return  f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
            
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
            super().__init__(tag, None, children, props)



    def to_html(self):
        if self.tag == None:
            raise ValueError
        if self.children == None:
            raise ValueError("no children")
        return  f'<{self.tag}{self.props_to_html()}>{self.loop_children()}</{self.tag}>'

    def loop_children(self):
        string = ""
        for child in self.children:
            string += child.to_html()
        return string

      