class Node:
    def __init__(self, is_leaf=False, num_keys=0, pairs=[], r_child=None, r_next=None):
        self.is_leaf = is_leaf

        self.num_keys = num_keys
        self.pairs = pairs
        self.r_child = r_child      # for non-leaf node
        self.r_next = r_next        # for leaf node
    
    def is_leaf(self):
        return self.is_leaf

    def set_leaf(self, bool):
        self.is_leaf = bool  