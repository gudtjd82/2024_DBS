class Node:
    def __init__(self, is_leaf=False, id=0, num_keys=0, pairs=[], rightmost=None):
        self.is_leaf = is_leaf

        self.id = id
        self.num_keys = num_keys
        self.pairs = pairs
        self.rightmost = rightmost      # non-leaf: rightmost child // leaf: right sibling
    
    def is_leaf(self):
        return self.is_leaf

    def set_leaf(self, bool):
        self.is_leaf = bool  
    
    def print_info(self):
        info = "{"
        info += "id: {}, ".format(self.id)
        info += "is_leaf: {}, ".format(self.is_leaf)
        info += "num_keys: {}, ".format(self.num_keys)
        info += "pairs: {}, ".format(self.pairs)
        info += "rightmost: {}}}".format(self.rightmost)

        print(info)