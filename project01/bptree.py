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
            print("ERROR: Insertion")
            return None, -1
        return node, pair_pos

def split(node=Node(), next_id=0):
    new_node = None
    degree = node.get_degree()
    

def insert(index_file="index.dat", input_file="input.csv"):
    meta_data, root, next_id = parse_index_file(index_file)
    input_pairs = parse_csv_file(input_file)

    degree = meta_data["b"]
    root_id = meta_data["root"]
    for pair in input_pairs:
        # tree가 비어있을 때
        if root_id == 0:
            new_node = Node(True, next_id)
            root_id = next_id
            next_id +=1
            if new_node.add_pair(pair) < 0:
                print("ERROR: Duplicated key")
                return None
            root = new_node
            continue
        
        # tree에 node가 존재할 때
        target_node, pair_pos = find_postion_to_insert(root, pair[0])
        if target_node.get_num_keys() < pair_pos+1:
            target_node.add_pair(pair)
        else:
            split(target_node, next_id)

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
