import math
from node import *

from utils import *

# Data File Creation
def create_bptree(file_name="index.dat", b=5):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write("@ Meta info.\n")
        file.write("b={}\n".format(b))
        file.write("root=0\n")
        file.write("\n")
        file.write("@ Node info.\n")
        file.write("# Node ID, Type (0: non-leaf, 1: leaf), Key Count, [Keys], [Child Node Pointers or Values]\n")

# Insertion
def find_postion_to_insert(node = Node(), key = 0):
    if not node.get_is_leaf():
        next_node = node.find_next_for_key(key)
        return find_postion_to_insert(next_node, key)
    else:
        pair_pos = node.find_pair_pos(key)
        if pair_pos < 0:
            print("ERROR: find positon to insert")
            return None, -1
        return node, pair_pos

def split_and_insert(node=Node(), pair=(), next_id=0):
    root = None
    degree = node.get_degree()
    left_num_keys = math.ceil(degree / 2)
    right_num_keys = node.get_num_keys()-left_num_keys
    
    # If node is full
    if node.get_num_keys() >= degree:
        left_pairs = node.get_pairs()[:left_num_keys]
        right_pairs = node.get_pairs()[left_num_keys:]

        right_node = Node(degree, node.get_is_leaf(), node.get_id(), right_num_keys, right_pairs, node.get_rightmost(), node.get_parent())

        left_node = Node(degree, node.get_is_leaf(), next_id, left_num_keys, left_pairs, right_node, node.get_parent())
        next_id +=1

        up_key = left_node.get_pairs()[-1][0]
        up_pair = [up_key, left_node]
        parent = node.get_parent()
        # root node가 아닐 때
        if parent is not None:
            if parent.change_child(node, right_node) < 0:
                print("ERROR: split and insert - change child")
                return None, next_id
            
            root, next_id = split_and_insert(node.get_parent(), up_pair, next_id)
        # root node일 때
        else:
            root = Node(degree, False, next_id, 1, [up_pair], right_node)
            next_id +=1
            left_node.set_parent(root)
            right_node.set_parent(root)

        if pair[0] < up_key:
            left_node.add_pair(pair)
        else:
            right_node.add_pair(pair)

        # split할 node가 non-leaf node일 경우
        if not node.get_is_leaf():
            # rightmost 정정
            left_node.set_rightmost(None)
            # 자식 노드의 parent 변경
            for pair in left_node.get_pairs():
                pair[1].set_parent(left_node)
            for pair in right_node.get_pairs():
                pair[1].set_parent(right_node)
        else:
            # rightmost 정정
            ls= node.get_left_sibling()     # todo: 다른 접근 방법 필요. 참조 문제 발생
            if ls is not None:
                print(ls.get_id())
                print(left_node.get_id())
                left_node.set_left_sibling(ls)
                ls.set_rightmost(left_node)
                print(ls.get_rightmost().get_id())
            right_node.set_left_sibling(left_node)
            
            rmst =right_node.get_rightmost()
            if rmst is not None:
                rmst.set_left_sibling(right_node)

            print(ls)
        
        return root, next_id
    # If node is not full
    else:
        node.add_pair(pair)
        return node.get_root(), next_id

def insert(index_file="index.dat", input_file="input.csv"):
    meta_data, root, next_id = parse_index_file(index_file)
    input_pairs = parse_csv_file(input_file)

    for input_pair in input_pairs:
        print(input_pair)

    degree = meta_data["b"]
    root_id = meta_data["root"]
    for pair in input_pairs:
        # tree가 비어있을 때
        if root_id == 0:
            new_node = Node(degree, True, next_id)
            root_id = next_id
            next_id +=1
            if new_node.add_pair(pair) < 0:
                print("ERROR: Duplicated key")
                return None
            root = new_node
            continue
        
        # tree에 node가 존재할 때
        target_node, pair_pos = find_postion_to_insert(root, pair[0])
        if target_node is None:
            return target_node
        if target_node.get_num_keys() < degree:
            target_node.add_pair(pair)
        else:
            root, next_id = split_and_insert(target_node, pair, next_id)
            if root is None:
                break
        
        print(f"{pair} 삽입 완료")
        print("==================================")
        print_tree(root)
        print("==================================")

    return root

# Deletion
def delete(index_file="index.dat", data_file="delete.csv"):
    print("deletion")
    # todo

# Single Key Search
def search_single(index_file="index.dat", key=0):
    print("search single key")
    # todo

# Ranged Search
def search_range(index_file="index.dat", start_key=0, end_key=0):
    print("search keys in range")
    # todo7

# print the B+ Tree structure
def print_tree(node, level=0):
    if node is None:
        print()
        return
    indent = '  ' * level  
    node_id = node.get_id()
    keys = [key for key, _ in node.get_pairs()]
    if node.get_parent() is not None:
        parent_id = node.get_parent().get_id()
        if node.get_is_leaf():
            rmst = node.get_rightmost()
            if rmst is None:
                rmst_id = 0
            else:
                rmst_id = rmst.get_id()
            l_sibling = node.get_left_sibling()
            if l_sibling is None:
                ls_id = 0
            else:
                ls_id = l_sibling.get_id()
            print(f"{indent}{parent_id} | Node ID: {node_id}, Keys: {keys}, Right: {rmst}")
            # print(f"{indent}{parent_id} | Node ID: {node_id}, Keys: {keys}, Left: {ls_id}, Right: {rmst_id}")
        else:
            print(f"{indent}{parent_id} | Node ID: {node_id}, Keys: {keys}")
    else:
        print(f"{indent}r | Node ID: {node_id}, Keys: {keys}")
    
    if not node.get_is_leaf():
        for key, child_node in node.get_pairs():
            if isinstance(child_node, Node):
                print_tree(child_node, level + 1)

        rightmost_child = node.get_rightmost()
        if isinstance(rightmost_child, Node):
            print_tree(rightmost_child, level + 1)
    else:
        pass
