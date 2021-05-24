class Node:
    def __init__(self, type, val = None, children = None):
        self.type = type    # string
        self.val = val
        self.children = children
    
    def get_json(self):
        content = {}
        content['type'] = self.type
        if self.children and any(self.children):
            content['children'] = []
            for child in self.children:
                if child:
                    content['children'].append(child.get_json())
        
        return content