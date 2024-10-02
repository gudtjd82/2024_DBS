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
    return_node = None

    degree = node.get_degree()
    min_num_keys = math.ceil((degree-1) / 2)

    # node.add_pair(pair)
    # If node is full
    if node.get_num_keys() > degree-1:
        left_pairs = node.get_pairs()[:min_num_keys]
        right_pairs = node.get_pairs()[min_num_keys:]
        
        right_node = node
        right_node.set_pairs(right_pairs)
        return_node = right_node
        

        left_node = Node(degree, node.get_is_leaf(), next_id, len(left_pairs), left_pairs, right_node, right_node.get_parent())
        next_id +=1
        
        up_key = left_node.get_pairs()[-1][0]
        up_pair = [up_key, left_node]
        parent = right_node.get_parent() # type: Node
        # root node가 아닐 때
        if parent is not None:
            parent.add_pair(up_pair)
            if parent.get_num_keys() > degree-1:
                root, next_id, return_node = split(parent, next_id)
            else:
                root = parent.get_root()
            
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
            left_node.set_rightmost(None)   
            # 자식 노드의 parent 변경
            for pair in left_node.get_pairs():
                pair[1].set_parent(left_node)
            for pair in right_node.get_pairs():
                pair[1].set_parent(right_node)
            if right_node.get_rightmost() is not None:
                right_node.get_rightmost().set_parent(right_node)
        # node가 leaf node일 경우
        else:
            # rightmost 정정
            left_node.set_left_sibling(right_node.get_left_sibling())
            left_node.set_rightmost(right_node)
            ln_ls= left_node.get_left_sibling() # type: Node
            if ln_ls is not None:
                ln_ls.set_rightmost(left_node)
            right_node.set_left_sibling(left_node)
        return root, next_id, return_node
    
    # If node is not full
    else:
        return node.get_root(), next_id, node

def insert_pairs(pairs=[], root=Node(), degree=0, root_id=0, next_id=0, debug=False):
    for pair in tqdm(pairs, desc="Inserting", unit="pair"):
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
        root, next_id, _ = split(target_node, next_id)
        if root is None:
            break

        # for debugging
        if debug:
            print(f"{pair[0]} 삽입 완료")
            print("==============================")
            print_tree(root)
            print(is_bptree(root, degree))
            print("==============================")
    
    
    return root, next_id

def insertion(index_file="index.dat", input_file="input.csv", debug=False):
    meta_data, root, next_id = parse_index_file(index_file)
    input_pairs = parse_csv_file(input_file)

    degree = meta_data["degree"]
    root_id = meta_data["root"]

    root, next_id = insert_pairs(input_pairs, root, degree, root_id, next_id, debug)

    # print("Fixing some problems...")
    # root, next_id = fix_all_probs(root, next_id)

    print("Saving nodes...")
    save_nodes_to_index_file(index_file, root, degree)
    
    print("Insertion completed successfully!")
    return root, next_id
    

# Deletion
def take_or_merge(node=Node(), next_id=0, debug=False):
    if not node:
        return None, next_id, node

    root = node.get_root()
    degree = node.get_degree()
    min_num_keys = math.ceil((degree-1) / 2)
    return_node = node
    
    # node가 부족한 경우
    if node.get_num_keys() < min_num_keys:
        left = node.get_left_sibling() # type: Node
        right = node.get_right_sibling() # type: Node

        parent = node.get_parent()  # type: Node
        # left sibling에서 빌려오기
        if left and left.get_num_keys() > min_num_keys:
            if debug:
                print("left sibling에서 빌려오기")

            left_parent = left.get_parent() # type: Node

            # left의 가장 큰 pair를 가져오기
            left_pair = left.get_pairs()[-1]
            left.delete_pair(left_pair)
            node.add_pair(left_pair)

            # 이동한 pair의 set_parent
            if not left.get_is_leaf():
                left_pair[1].set_parent(node)

            # parent key 수정 - left_parent2 == parent2가 될 때까지
            left2 = left
            node2 = node
            left_parent2 = left_parent
            parent2 = parent
            if left_parent2:
                idx = left_parent2.find_child_idx(left2)
                # left가 rightmost가 아닌 경우
                if idx < left_parent2.get_num_keys():
                    while left2 != node2:
                        if left_parent2:
                            idx = left_parent2.find_child_idx(left2)
                            n_k = left2.get_pairs()[-1][0]
                            left_parent2.set_pairs_at(idx, [n_k, left2])
                        else:
                            break

                        left2 = left_parent2
                        node2 = parent2
                        left_parent2 = left_parent2.get_parent()    # type: Node
                        parent2 = parent2.get_parent()    # type: Node
                # left가 rightmost인 경우 (left_parent는 rightmost가 아님)
                else:
                    n_k = left2.get_pairs()[-1][0]
                    while left2 != node2:
                        left2 = left_parent2
                        node2 = parent2
                        left_parent2 = left_parent2.get_parent()    # type: Node
                        parent2 = parent2.get_parent()    # type: Node

                        if left_parent2:
                            idx = left_parent2.find_child_idx(left2)
                            left_parent2.set_pairs_at(idx, [n_k, left2])
                        else:
                            break


            # left node가 rightmost가 존재하는 non-leaf node일 경우
            if not node.get_is_leaf() and left.get_rightmost():
                # left의 rightmost에 있는 pair를 node의 두 번째 pair에 insert -> split
                left_rightmost = left.get_rightmost()
                left.set_rightmost(None)

                insert_pos_node = node.get_pairs()[1][1]    # type: Node
                for pair in left_rightmost.get_pairs():
                    insert_pos_node.add_pair(pair)
                root, next_id, _ = split(insert_pos_node, next_id)

            return root, next_id, return_node

        # right sibling에서 빌려오기
        elif right and right.get_num_keys() > min_num_keys:
            if debug:
                print("right sibling에서 빌려오기")

            right_parent = right.get_parent() # type: Node

            # right의 가장 작은 pair를 가져오기
            right_pair = right.get_pairs()[0]
            right.delete_pair(right_pair)
            node.add_pair(right_pair)

            # 이동한 pair의 set_parent
            
            if not right.get_is_leaf():
                right_pair[1].set_parent(node)

            # parent key 수정 - parent_2 == right_parent2가 될 때까지
            right2 = right
            node2 = node
            right_parent2 = right_parent
            parent2 = parent
            if parent2:
                idx = parent2.find_child_idx(node2)
                # node가 rightmost가 아닌 경우
                if idx < parent2.get_num_keys():
                    while right2 != node2:
                        if parent2:
                            idx = parent2.find_child_idx(node2)
                            n_k = node2.get_pairs()[-1][0]
                            parent2.set_pairs_at(idx, [n_k, node2])
                        else:
                            break

                        node2 = parent2
                        right2 = right_parent2
                        parent2 = parent2.get_parent()    # type: Node
                        right_parent2 = right_parent2.get_parent()    # type: Node
                # node가 rightmost인 경우
                else:
                    n_k = node2.get_pairs()[-1][0]
                    while right2 != node2:
                        node2 = parent2
                        right2 = right_parent2
                        parent2 = parent2.get_parent()  # type: Node
                        right_parent2 = right_parent2.get_parent()  # type: Node

                        if parent2:
                            idx = parent2.find_child_idx(node2)
                            parent2.set_pairs_at(idx, [n_k, node2])
                        else:
                            break

            # node가 rightmost가 존재하는 non-leaf node일 경우
            if not node.get_is_leaf() and node.get_rightmost():
                # node의 rightmost에 있는 pair를 insert
                rightmost = node.get_rightmost()
                node.set_rightmost(None)

                insert_pos_node = node.get_pairs()[-1][1]   # type: Node
                for pair in rightmost.get_pairs():
                    insert_pos_node.add_pair(pair)
                root, next_id, _ = split(insert_pos_node, next_id)

            return root, next_id, return_node

        # left sibling과 병합
        elif left and left.get_num_keys() + node.get_num_keys() < degree:
            if debug:
                print("left sibling과 병합")

            return_node = node

            left_parent = left.get_parent() # type: Node

            if node.get_is_leaf():
                # node에 left를 병합 후 parent 수정
                for left_pair in left.get_pairs():
                    node.add_pair(left_pair)
                    if node.get_num_keys() > degree-1:
                        return None, next_id, return_node
                
                # leaf node 간의 pointer 수정 
                l_ls = left.get_left_sibling()  # type: Node
                node.set_left_sibling(l_ls)
                if l_ls:
                    l_ls.set_rightmost(node)
                
                # parent에서 left node의 pair 삭제
                if left_parent:
                    left_parent.delete_child(left)

                # parent key 수정 - left_parent2 == parent2가 될 때까지
                left2 = left_parent
                node2 = parent
                left_parent2 = left_parent.get_parent()
                parent2 = parent.get_parent()
                while left2 != node2:
                    if left_parent2:
                        idx = left_parent2.find_child_idx(left2)
                        n_k = left2.get_pairs()[-1][0]
                        left_parent2.set_pairs_at(idx, [n_k, left2])
                    else:
                        break

                    left2 = left_parent2
                    node2 = parent2
                    left_parent2 = left_parent2.get_parent()    # type: Node
                    parent2 = parent2.get_parent()    # type: Node

                return take_or_merge(left_parent, next_id)
            # non-leaf node일 경우
            else:
                # 일단 node에 left를 병합 + set_parent -> left 삭제 -> parent key 수정 -> left node에 rightmost가 존재하면, left의 rightmost와 node의 leftmost 합치기 -> split 
                insert_pos = left.get_num_keys()
                node_rightmost = node.get_rightmost()
                left_rightmost = left.get_rightmost()

                # node에 left를 병합
                for pair in left.get_pairs():
                    node.add_pair(pair)
                    pair[1].set_parent(node)

                # left 삭제
                left_parent.delete_child(left)

                # parent key 수정
                left2 = left_parent
                node2 = parent
                left_parent2 = left_parent.get_parent()
                parent2 = parent.get_parent()
                while left2 != node2:
                    if left_parent2:
                        idx = left_parent2.find_child_idx(left2)
                        n_k = left2.get_pairs()[-1][0]
                        left_parent2.set_pairs_at(idx, [n_k, left2])
                    else:
                        break

                    left2 = left_parent2
                    node2 = parent2
                    left_parent2 = left_parent2.get_parent()    # type: Node
                    parent2 = parent2.get_parent()    # type: Node

                # left node에 rightmost가 존재하면
                if left_rightmost:
                    # left의 rightmost와 node의 leftmost 합치기
                    insert_pos_node = node.get_pairs()[insert_pos][1]   # type: Node
                    for pair in left_rightmost.get_pairs():
                        insert_pos_node.add_pair(pair)
                    # split
                    root, next_id, _ = split(insert_pos_node, next_id)

                return root, next_id, return_node
        
        # right sibling과 병합        
        elif right and right.get_num_keys() + node.get_num_keys() < degree:
            if debug:
                print("right sibling과 병합")

            return_node = right

            right_parent = right.get_parent() # type: Node

            if node.get_is_leaf():
                # right에 node를 병합 후 parent 수정
                for pair in node.get_pairs():
                    right.add_pair(pair)
                    if right.get_num_keys() > degree-1:
                        return None, next_id, return_node
                
                # leaf node 간의 pointer 수정 
                n_ls = node.get_left_sibling()  # type: Node
                right.set_left_sibling(n_ls)
                if n_ls:
                    n_ls.set_rightmost(right)
                
                # parent에서 pair 삭제
                if parent:
                    parent.delete_child(node)
                
                # parent key 수정 - right_parent2 == parent2가 될 때까지
                node2 = parent
                right2 = right_parent
                parent2 = parent.get_parent()
                right_parent2 = right_parent.get_parent()
                while right2 != node2:
                    if parent2:
                        idx = parent2.find_child_idx(node2)
                        n_k = node2.get_pairs()[-1][0]
                        parent2.set_pairs_at(idx, [n_k, node2])
                    else:
                        break

                    node2 = parent2
                    right2 = right_parent2
                    parent2 = parent2.get_parent()    # type: Node
                    right_parent2 = right_parent2.get_parent()    # type: Node

                return take_or_merge(parent, next_id)
            # non-leaf node일 경우
            else:
                # 일단 right에 node를 병합 -> node 삭제 -> parent key 수정 -> node에 rightmost가 존재하면, node의 rightmost와 right의 leftmost 합치기 -> set_parent -> split 
                insert_pos = node.get_num_keys()
                node_rightmost = node.get_rightmost()
                
                # right에 node를 병합
                for pair in node.get_pairs():
                    right.add_pair(pair)
                    pair[1].set_parent(right)

                # node 삭제
                parent.delete_child(node)

                # parent key 수정 - right_parent2 == parent2가 될 때까지
                node2 = parent
                right2 = right_parent
                parent2 = parent.get_parent()
                right_parent2 = right_parent.get_parent()
                while right2 != node2:
                    if parent2:
                        idx = parent2.find_child_idx(node2)
                        n_k = node2.get_pairs()[-1][0]
                        parent2.set_pairs_at(idx, [n_k, node2])
                    else:
                        break

                    node2 = parent2
                    right2 = right_parent2
                    parent2 = parent2.get_parent()    # type: Node
                    right_parent2 = right_parent2.get_parent()    # type: Node
                
                if node_rightmost:
                    # node의 rightmost와 right의 leftmost 합치기
                    insert_pos_node = right.get_pairs()[insert_pos][1]
                    for pair in node_rightmost.get_pairs():
                        insert_pos_node.add_pair(pair)
                    # split
                    root, next_id, _ = split(insert_pos_node, next_id)
                
                return root, next_id, return_node
    return root, next_id, return_node

def delete_keys(keys=[], root=Node(), next_id=0, debug=False):
    for del_k in tqdm(keys, desc="Deleting", unit="key"):
        target_node, target_pair, _ = find_key_from_root(root, del_k)

        if target_node is None:
            print(f"ERROR: deletion - CAN'T FIND {del_k}")
            continue
        
        if target_node.delete_pair(target_pair) < 0:
            print("ERROR: deletion - delete pair")
            return None

        root, next_id, _ = take_or_merge(target_node, next_id, debug)

        while root.get_num_children() == 1:
            root = root.get_child_at(0)
            root.set_parent(None)

        # for debugging
        if debug:
            bptree_check = is_bptree(root, root.get_degree())
            print(f"deletion completed: {del_k}")
            print("==============================")
            print_tree(root)
            print(bptree_check)
            print("==============================")

        # if not bptree_check:
        #     print("Deletion Error! - NOT B+ Tree")
        #     return root, next_id

        if not root:
            print("Deletion Error! - fix all probs")
            return root, next_id

    return root, next_id

def deletion(index_file="index.dat", delete_file="delete.csv", debug=False):
    meta_data, root, next_id = parse_index_file(index_file)

    del_keys = [int(k[0]) for k in parse_csv_file(delete_file)]

    root, next_id = delete_keys(del_keys, root, next_id, debug)

    print("Fixing some problems...")
    is_safe, root, next_id = fix_all_probs(root, next_id)
    
    if not is_safe:
        print("Deletion Error - fix_all_probs failed.")
        return root, next_id

    print("Saving nodes...")
    save_nodes_to_index_file(index_file, root, root.get_degree())

    print("Deletion completed successfully!")
    return root, next_id


# Single Key Search
def find_key_from_root(node=Node(), key=0, path_nodes=[]):
    if not node:
        return None, None, None
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
def check_and_fix_node(node=Node(), next_id=0, num_keys_range=(), children_range=(), level=0, leaf_levels=[], fix=False, debug=False):
    if not node:
        if not fix:
            return True
        else:
            return True, None, next_id, node
    
    is_safe = True
    root = node.get_root()
    prob_node = node

    # root와 leaf가 아닌 node의 children 수 확인
    if node != root and not node.get_is_leaf():
        if node.get_num_children() > children_range[1]:
            if not fix:
                print("root가 아닌 non-leaf node의 children 수 확인 -> FALSE")
                return False
            else:
                root, next_id, prob_node = split(node, next_id)
                is_safe, root, next_id, prob_node = check_and_fix_node(node=prob_node.get_parent(), next_id=next_id, num_keys_range=num_keys_range,  children_range=children_range, level=level-1, leaf_levels=leaf_levels, fix=fix, debug=debug)

                if not is_safe:
                    return is_safe, root, next_id, prob_node

        elif node.get_num_children() < children_range[0]:
            if not fix:
                print("root가 아닌 non-leaf node의 children 수 확인 -> FALSE")
                return False
            else:
                root, next_id, prob_node = take_or_merge(node, next_id, debug)
                is_safe, root, next_id, prob_node = check_and_fix_node(node=prob_node.get_parent(), next_id=next_id, num_keys_range=num_keys_range, children_range=children_range, level=level-1, leaf_levels=leaf_levels, fix=fix, debug=debug)

                if not is_safe:
                    return is_safe, root, next_id, prob_node
                # return False, root, next_id, prob_node
    
    # node의 key 수(= value 수) 확인
    if node != root:
        if node.get_num_keys() > num_keys_range[1]:
            if not fix:
                print("node의 value 수 확인 -> FALSE")
                return False
            else:
                root, next_id, prob_node = split(node, next_id)
                is_safe, root, next_id, prob_node = check_and_fix_node(node=prob_node.get_parent(), next_id=next_id, num_keys_range=num_keys_range, children_range=children_range, level=level-1, leaf_levels=leaf_levels, fix=fix, debug=debug)

                if not is_safe:
                        return is_safe, root, next_id, prob_node
                # return False, root, next_id, prob_node
        elif node.get_num_keys() < num_keys_range[0]:
            if not fix:
                print("node의 value 수 확인 -> FALSE")
                return False
            else:
                root, next_id, prob_node = take_or_merge(node, next_id, debug)
                is_safe, root, next_id, prob_node = check_and_fix_node(node=prob_node.get_parent(), next_id=next_id, num_keys_range=num_keys_range, children_range=children_range, level=level-1, leaf_levels=leaf_levels, fix=fix, debug=debug)

                if not is_safe:
                        return is_safe, root, next_id, prob_node
                # return False, root, next_id, prob_node
    else:
        while root.get_num_children() == 1:
            root = root.get_child_at(0)
            root.set_parent(None)

    if node.get_is_leaf():
        # 첫 번째 leaf node의 level을 저장
        if not leaf_levels:
            leaf_levels.append(level)
        # 모든 leaf node는 같은 level에 있어야 함
        elif leaf_levels[0] != level:
            print("leaf node의 level이 모두 같은지 확인 -> FALSE")
            if not fix:
                return False
            else:
                return False, None, next_id, prob_node

        # 오름차순 확인
        if node.get_rightmost() and node.get_rightmost().get_is_leaf():
            if node.get_pairs()[-1][0] > node.get_rightmost().get_pairs()[0][0]:
                print("오름차순 정렬 확인 -> FALSE")
                if not fix:
                    return False
                else:
                    return False, None, next_id, prob_node
        if not fix:
            return True
        else:
            return True, root, next_id, prob_node
    
    return True, root, next_id, prob_node

def check_all_nodes(node=Node(), next_id=0, num_keys_range=(), children_range=(), level=0, leaf_levels=[], fix=False, debug=False):
    
    if not fix:
        is_safe =  check_and_fix_node(node=node, next_id=next_id, num_keys_range=num_keys_range, children_range=children_range, level=level, leaf_levels=leaf_levels, fix=fix, debug=debug)
        if not is_safe:
            return is_safe
    else:
        is_safe, root, next_id, prob_node = check_and_fix_node(node=node, next_id=next_id, num_keys_range=num_keys_range, children_range=children_range, level=level, leaf_levels=leaf_levels, fix=fix, debug=debug)

        if not is_safe:
            return is_safe, root, next_id, prob_node

    # children에 대해 순회하며 check
    if is_safe and not node.get_is_leaf():
        for k, child in node.get_pairs():
            if not child:
                continue
            
            if not fix:
                if not check_all_nodes(node=child, num_keys_range=num_keys_range, children_range=children_range, level=level + 1, leaf_levels=leaf_levels, fix=fix):
                    return False
            else:
                is_safe, root, next_id, prob_node = check_all_nodes(node=child, num_keys_range=num_keys_range, children_range=children_range, level=level+1, leaf_levels=leaf_levels, next_id=next_id, fix=fix, debug=debug)
                if not is_safe:
                    return is_safe, root, next_id, prob_node
                if not root:
                    print("check error!")
                    return check, root, next_id, prob_node
    if not fix:
        return True
    else:
        return True, root, next_id, prob_node

# root를 인자로 받아 B+ tree의 문제점을 찾고 그것을 고치기를 반복
def fix_all_probs(node=Node(), next_id=0):
    degree = node.get_degree()
    num_keys_range = ((degree-1)//2, degree-1)
    children_range = (degree//2, degree)

    root = None

    leaf_levels = []

    is_safe = False
    # while not is_safe:
        # node에 return_node를 넣어 이어서 순회
    for _ in range(3):
        is_safe, root, next_id, prob_node = check_all_nodes(node=node, next_id=next_id, num_keys_range=num_keys_range, children_range=children_range, level=0, leaf_levels=leaf_levels, fix=True)

    return is_safe, root, next_id

def is_bptree(root, degree, next_id=0):
    if not root:
        return False 

    # 빈 리스트로 리프 노드의 레벨을 기록하여 같은 레벨에 있는지 확인
    leaf_levels = []
    
    # 루트는 예외적으로 최소 1개의 키를 가져야 함
    num_keys_range = ((degree-1)//2, degree-1)
    children_range = (degree//2, degree)

    return check_all_nodes(node=root, next_id=next_id, num_keys_range=num_keys_range, children_range=children_range, level=0, leaf_levels=leaf_levels, fix=False)
    # return check_and_fix_node(node=root, num_keys_range=num_keys_range, children_range=children_range, level=0, leaf_levels=leaf_levels)

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
