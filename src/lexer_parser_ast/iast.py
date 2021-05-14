class Node:
    def __init__(self, type, val = None, children = None):
        self.type = type    # string
        self.val = val
        self.children = children
    
    def get_json(self):
        content = {}
        content['type'] = self.type
        if self.children:
            content['children'] = []
            for child in self.children:
                content['children'].append(child.get_json())
        
        return content