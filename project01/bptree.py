import math
from tqdm import tqdm
from node import *

from utils import *

# Data File Creation
def create_index_file(file_name="index.dat", degree=5):
    new_index_file(index_file=file_name, degree=degree)

# Insertion
def find_postion_to_insert(node = Node(), key = 0):
    if not node.get_is_leaf():
        next_node = node.find_next_for_key(key)
        if next_node is None:
            return node, -1
        return find_postion_to_insert(next_node, key)
    else:
        pair_pos = node.find_pair_pos(key)
        if pair_pos < 0:
            print("ERROR: find positon to insert")
            return None, -1
        return node, pair_pos

def split(node=Node(), next_id=0):
    root = None
    degree = node.get_degree()
    min_num_keys = math.ceil((degree-1) / 2)
    
    # node.add_pair(pair)
    # If node is full
    if node.get_num_keys() > degree-1:
        left_pairs = node.get_pairs()[:min_num_keys]
        right_pairs = node.get_pairs()[min_num_keys:]
        
        left_node = node
        left_node.set_pairs(left_pairs)
        

        right_node = Node(degree, node.get_is_leaf(), next_id, len(right_pairs), right_pairs, left_node.get_rightmost(), left_node.get_parent())
        next_id +=1
        
        if not node.get_is_leaf():
            # right node의 leftmost를 left node의 rightmost로 이동
            leftmost_of_right_node = right_pairs[0][1]
            right_pairs[0][1] = None
            right_node.set_pairs(right_pairs)
            left_node.set_rightmost(leftmost_of_right_node)

        up_key = right_node.get_pairs()[0][0]
        up_pair = [up_key, left_node]
        parent = left_node.get_parent() # type: Node
        # root node가 아닐 때
        if parent is not None:
            right_node.set_parent(parent)
            idx_of_left = parent.find_child_idx(left_node)
            parent.insert_child(idx_of_left, right_node)

            parent.add_pair(up_pair)
            if parent.get_num_keys() > degree-1:
                root, next_id = split(parent, next_id)
            else:
                root = parent.get_root()
            # idx_of_left = parent.find_child_idx(left_node)
            # parent.insert_child(idx_of_left+1, right_node)
        # root node일 때
        else:
            root = Node(degree, False, next_id, 1, [up_pair], right_node)
            next_id +=1
            left_node.set_parent(root)
            right_node.set_parent(root)
        
        # rightmost, parent 등의 pointer 정정
        # node가 non-leaf node일 경우
        if not node.get_is_leaf():
            # rightmost 정정
            left_node.set_rightmost(None)   # todo: rightnode를 어디에 할당할지
            # 자식 노드의 parent 변경
            for pair in left_node.get_pairs():
                pair[1].set_parent(left_node)
            for pair in right_node.get_pairs():
                if pair[1] is not None:
                    pair[1].set_parent(right_node)
        # node가 leaf node일 경우
        else:
            # rightmost 정정
            right_node.set_left_sibling(left_node)
            right_node.set_rightmost(left_node.get_rightmost())
            left_node.set_rightmost(right_node)
            rn_rmst= right_node.get_rightmost()
            if rn_rmst is not None:
                rn_rmst.set_left_sibling(right_node)
        
        return root, next_id
    
    # If node is not full
    else:
        return node.get_root(), next_id

def insert(index_file="index.dat", input_file="input.csv"):
    meta_data, root, next_id = parse_index_file(index_file)
    input_pairs = parse_csv_file(input_file)

    degree = meta_data["degree"]
    root_id = meta_data["root"]
    for pair in tqdm(input_pairs, desc="Insertion", unit="pair"):
        # tree가 비어있을 때
        if root_id == 0:
            new_node = Node(degree, True, next_id)
            root_id = next_id
            next_id +=1
            if new_node.add_pair(pair) < 0:
                continue
            root = new_node
            continue
        
        # tree에 node가 존재할 때
        target_node, pair_pos = find_postion_to_insert(root, pair[0])
        if target_node is None:
            return target_node
        # 새로운 node 필요
        if target_node is not None and pair_pos < 0:
            num_children = target_node.get_num_children()
            target_pairs = target_node.get_pairs()
            if num_children < degree:
                # target node에 child node 추가
                c_is_leaf = target_pairs[0][1].get_is_leaf()
                c_left = target_pairs[-1][1]
                child = Node(degree, c_is_leaf, next_id, 0, [], parent=target_node)
                next_id +=1
                if c_is_leaf:
                    c_rightmost = c_left.get_rightmost()
                    c_left.set_rightmost(child)
                    child.set_left_sibling(c_left)
                    if c_rightmost is not None:
                        child.set_rightmost(c_rightmost)
                
                target_node = child
        if target_node is None:
            print("ERROR: target node is None")
            return None
        
        target_node.add_pair(pair)
        root, next_id = split(target_node, next_id)
        if root is None:
            break

        # for debugging
        print(f"{pair[0]} 삽입 완료")
        print("==============================")
        print_tree(root)
        print("==============================")
    
    save_nodes_to_index_file(index_file, root, degree)
    # save_nodes_to_index_file(index_file="index_test.dat", root=root, degree=degree)
    return root

# Deletion
def delete(index_file="index.dat", data_file="delete.csv"):
    print("deletion")
    # todo

# Single Key Search
def find_key_from_root(node=Node(), key=0, path_nodes=[]):
    if not node.get_is_leaf():
        next_node = node.find_next_for_key(key)
        path_nodes.append(next_node)
        return find_key_from_root(next_node, key, path_nodes)
    else:
        pair = node.find_key(key)
        if pair is None:
            print("ERROR: Single Key Search - find_key")
            return None, None, path_nodes
        return node, pair, path_nodes
    
def search_single(index_file="index.dat", key=0):
    meta_data, root, next_id = parse_index_file(index_file)

    path_nodes = []
    path_nodes.append(root)

    found_node, found_pair, path_nodes = find_key_from_root(root, key, path_nodes)
    if found_node is None:
        print("NOT FOUND")
        return None
    
    for node in path_nodes[:-1]:
        node.print_all_keys()
    
    print(found_pair[1])

    return found_node, found_pair, path_nodes


# Ranged Search
def search_range(index_file="index.dat", start_key=0, end_key=0):
    meta_data, root, next_id = parse_index_file(index_file)
    degree = meta_data["degree"]

    start_node, start_pos = find_postion_to_insert(root, start_key)
    if start_pos < degree-1:
        pairs = start_node.get_pairs()
        for pair in pairs[start_pos:]:
            if pair[0] > end_key:
                return
            print(f"{pair[0]}, {pair[1]}")
    
    next_node = start_node.get_rightmost()
    while next_node is not None:
        pairs = next_node.get_pairs()
        for pair in pairs:
            if pair[0] > end_key:
                return
            print(f"{pair[0]}, {pair[1]}")
        next_node = next_node.get_rightmost()

# B+ Tree인지 확인
def is_bptree(root, degree):
    if not root:
        return False 

    def check_node(node=Node(), key_range=(), children_range=(), level=0, leaf_levels=[]):
        # root와 leaf가 아닌 node의 children 수 확인
        if node != root and not node.get_is_leaf():
            if node.get_num_children() > children_range[1] or node.get_num_children() < children_range[0]:
                print("root와 leaf가 아닌 node의 children 수 확인 -> FALSE")
                return False
        
        # leaf node의 value 수 확인
        if node.get_is_leaf():
            if node.get_num_keys() > key_range[1] or node.get_num_keys() < key_range[0]:
                print("leaf node의 value 수 확인 -> FALSE")
                return False

            # 첫 번째 leaf node의 level을 저장
            if not leaf_levels:
                leaf_levels.append(level)
            # 모든 leaf node는 같은 level에 있어야 함
            elif leaf_levels[0] != level:
                print("leaf node의 level이 모두 같은지 확인 -> FALSE")
                return False

            # 오름차순 확인
            if node.get_rightmost() and node.get_rightmost().get_is_leaf():
                if node.get_pairs()[-1][0] > node.get_rightmost().get_pairs()[0][0]:
                    print("오름차순 정렬 확인 -> FALSE")
                    return False
            return True


        if not node.is_leaf:
            for k, child in node.get_pairs():
                if not check_node(child, key_range, children_range, level + 1, leaf_levels):
                    return False

        return True

    # 빈 리스트로 리프 노드의 레벨을 기록하여 같은 레벨에 있는지 확인
    leaf_levels = []
    
    # 루트는 예외적으로 최소 1개의 키를 가져야 함
    key_range = ((degree-1)//2, degree-1)
    children_range = (degree//2, degree)
    return check_node(root, key_range, children_range, 0, leaf_levels)

# print the B+ Tree structure
def print_tree(node, level=0, total_nodes_num=0):
    if node is None:
        return
    indent = '     ' * level  
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
            print(f"{indent}{parent_id} | Node ID: {node_id}, Keys: {keys}, Right: {rmst_id}")
            # print(f"{indent}{parent_id} | Node ID: {node_id}, Keys: {keys}, Left: {ls_id}, Right: {rmst_id}")
        else:
            print(f"{indent}{parent_id} | Node ID: {node_id}, Keys: {keys}")
    else:
        print(f"{indent}r | Node ID: {node_id}, Keys: {keys}")
    
    total_nodes_num +=1
    
    if not node.get_is_leaf():
        for key, child_node in node.get_pairs():
            if isinstance(child_node, Node):
                total_nodes_num = print_tree(child_node, level + 1, total_nodes_num)

        rightmost_child = node.get_rightmost()
        if isinstance(rightmost_child, Node):
            total_nodes_num = print_tree(rightmost_child, level + 1, total_nodes_num)
        return total_nodes_num
    else:
        return total_nodes_num
