class Node:
    def __init__(self, degree=1, is_leaf=False, node_id=0, num_keys=0, pairs=[], rightmost=None, parent=None, left_sibling=None):
        self.degree = degree
        self.is_leaf = is_leaf
        self.node_id = node_id
        self.num_keys = num_keys
        self.pairs = pairs
        self.rightmost = rightmost      # non-leaf: rightmost child // leaf: right sibling
        self.parent = parent
        self.left_sibling = left_sibling
    
    def __hash__(self):
        return hash(self.node_id)

    def __eq__(self, other):
        return isinstance(other, Node) and self.node_id == other.get_id()

    def __repr__(self):
        # info = "{} ".format(self.parent.get_id())
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
            print(f"Duplicated key: {pair}")
            return -1

        self.pairs.append(pair)
        self.pairs.sort(key=lambda pair: pair[0])
        self.num_keys +=1
        return 0
    
    def delete_pair(self, del_pair=(1, 100)):
        for i, pair in enumerate(self.pairs):
            if pair == del_pair:
                del self.pairs[i]
                self.num_keys -=1
                return 0
        return -1

    def find_next_for_key(self, key):
        next = None
        for pair in self.pairs:
            if key <= pair[0]:
                next = pair[1]
                break
        if next is None:
            next = self.rightmost
        return next

    def find_pair_pos(self, key):
        i = 0
        for pair in self.pairs:
            if key <= pair[0]:
                return i
            i +=1
        return i

    def find_key(self, key):
        for pair in self.pairs:
            if key == pair[0]:
                return pair
        return None

    def find_child_idx(self, child):
        for i, pair in enumerate(self.pairs):
            if child in pair:
                return i
        if self.rightmost == child:
            return self.degree-1
        return -1
    
    def insert_child(self, idx, child):
        if idx < 0:
            return -1
        # pair에 insert
        elif idx < self.num_keys-1:
            self.pairs[idx][1] = child
        else:
            self.rightmost = child
    
    def delete_child(self, child):
        for i, pair in enumerate(self.pairs):
            if child in pair:
                self.delete_pair(pair)
                return 0
        if self.rightmost == child:
            self.rightmost = None
            return 0
        return -1
    # 안 쓰이면 삭제해도 됨
    def change_child(self, old, new):
        for pair in self.pairs:
            if old in pair:
                pair[1] = new
                return 0
        if self.rightmost == old:
            self.rightmost = new
            return 0
        return -1

    def print_all_keys(self):
        keys_str = ""
        for pair in self.pairs:
            keys_str += f"{pair[0]}, "

        print(keys_str[:-2])
    
    def get_root(self):
        temp = self
        while True:
            if temp.get_parent() is None:
                break
            temp = temp.get_parent()
        return temp

    def get_num_children(self):
        if self.rightmost is not None:
            return self.num_keys + 1
        else:
            return self.num_keys
        
    def get_degree(self):
        return self.degree
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
    def get_parent(self):
        return self.parent
    def get_left_sibling(self):
        return self.left_sibling

    def set_leaf(self, bool):
        self.is_leaf = bool  

    def set_pairs(self, pairs):
        self.pairs = pairs
        self.num_keys = len(pairs)

    def set_pairs_at(self, idx, pair):
        self.pairs[idx] = pair

    def set_rightmost(self, rightmost):
        self.rightmost = rightmost
    def set_parent(self, parent):
        self.parent = parent
    def set_left_sibling(self, ls):
        self.left_sibling = ls


