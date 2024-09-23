class Node:
    def __init__(self, is_leaf=False, node_id=0, num_keys=0, pairs=[], rightmost=None):
        self.is_leaf = is_leaf

        self.node_id = node_id
        self.num_keys = num_keys
        self.pairs = pairs
        self.rightmost = rightmost      # non-leaf: rightmost child // leaf: right sibling
    
    def __repr__(self):
        info = "{"
        info += "id: {}, ".format(self.node_id)
        info += "is_leaf: {}, ".format(self.is_leaf)
        info += "num_keys: {}, ".format(self.num_keys)

        info += "pairs: {"
        for pair in self.pairs:
            if isinstance(pair[1], int):
                info += "{}, ".format(pair)
            else:
                info += "({}, node({})), ".format(pair[0], pair[1].get_id())
        info += "}, "
        
        if self.rightmost is not None:
            if isinstance(self.rightmost, int):
                info += "rightmost: {}}}".format(self.rightmost)
            else:
                info += "rightmost: node({})}}".format(self.rightmost.get_id())

        return info
    
    def get_is_leaf(self):
        return self.is_leaf

    def get_id(self):
        return self.node_id
    
    def get_pairs(self):
        return self.pairs
    
    def get_rightmost(self):
        return self.rightmost
    
    def set_leaf(self, bool):
        self.is_leaf = bool  
    
    def set_pairs(self, pairs):
        self.pairs = pairs
    
    def set_rightmost(self, rightmost):
        self.rightmost = rightmost


def draw_tree(root=Node()):
    if root.get_is_leaf():
        info += "pairs: {"
        for pair in root.get_pairs():
            if isinstance(pair[1], int):
                info += "{}, ".format(pair)
            else:
                info += "({}, node({})), ".format(pair[0], pair[1].get_id())
        info += "}, "
        print("{}:{}".format(root.get_id(), root.get_pairs()))
    else:
        print("{}:{}".format(root.get_id(), root.get_pairs()))
        pointers = [pair[1] for pair in root.get_pairs()]
        pointers.append(root.get_rightmost())
        for p in pointers:
            draw_tree(p)