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

    def is_duplicated_key(self, new_key):
        for pair in self.pairs:
            if pair[0] == new_key:
                return True
        return False
    
    def add_pair(self, pair=(1, 100)):
        if self.is_duplicated_key(pair[0]):
            return -1

        self.pairs.append(pair)
        self.pairs.sort(key=lambda pair: pair[0])
        self.num_keys +=1
        return 0
    
    def get_is_leaf(self):
        return self.is_leaf
    def get_id(self):
        return self.node_id
    def get_num_keys(self):
        return self.num_keys
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


def print_tree(node, level=0):
    if node is None:
        print()
        return
    indent = '  ' * level  
    node_id = node.get_id()
    keys = [key for key, _ in node.get_pairs()]
    print(f"{indent}Node ID: {node_id}, Keys: {keys}")
    
    if not node.get_is_leaf():
        for key, child_node in node.get_pairs():
            if isinstance(child_node, Node):
                print_tree(child_node, level + 1)

        rightmost_child = node.get_rightmost()
        if isinstance(rightmost_child, Node):
            print_tree(rightmost_child, level + 1)
    else:
        pass
