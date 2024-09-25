import csv
import re
from collections import deque
from node import *
# from bptree import *
'''
@ Meta info.
b=4
root=1

@ Node info.
# Node ID, Type (0: non-leaf, 1: leaf), Key Count, [Keys], [Child Node Pointers or Values]
1, 0, 2, [10, 20], [2, 3, 4]
2, 1, 2, [5, 8], [100, 150]  
3, 1, 2, [12, 18], [200, 250]
4, 1, 1, [25], [300]
'''

def new_index_file(index_file="index.dat", degree=5):
    with open(index_file, 'w', encoding='utf-8') as file:
        file.write("@ Meta info.\n")
        file.write("degree={}\n".format(degree))
        file.write("root=0\n")
        file.write(f'nodes_num=0\n')
        file.write("\n")
        file.write("@ Node info.\n")
        file.write("# Node ID, Type (0: non-leaf, 1: leaf), Key Count, [Keys], [Child Node Pointers or Values]\n")

def parse_index_file(index_file="index.dat"):
    # todo
    meta_data = {}
    degree = 0

    nodes = []          # 필요 없으면 삭제
    root_node = None
    nodes_dict = {}     # id로 node를 찾기 위한 dict
    next_id = 0

    parsing_meta = False
    parsing_nodes = False

    pattern = r'''
        \s*              # 공백 무시
        (                 # 그룹 시작
            \[.*?\]       # 대괄호로 묶인 부분 (비욕심 많은 매칭)
            |             # 또는
            [^,]+         # 쉼표가 아닌 문자들
        )
        \s*              # 공백 무시
        (?:,|$)          # 쉼표 또는 줄 끝
    '''
    with open(index_file, 'r', encoding='utf-8') as dat_file:
        file_iter = iter(dat_file)
        for line in file_iter:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue


            if "@ Meta info." in line:
                parsing_meta = True
                parsing_nodes = False
                continue
            elif "@ Node info." in line:
                parsing_nodes = True
                parsing_meta = False
                continue
            
            if parsing_meta:
                k, v = line.split("=")
                meta_data[k.strip()] = int(v)
            elif parsing_nodes:
                tokens = re.findall(pattern, line, re.VERBOSE)
                tokens = [token.strip() for token in tokens]

                node_id = int(tokens[0])
                if node_id >= next_id:
                    next_id = node_id
                
                degree = meta_data["degree"]
                is_leaf = bool(int(tokens[1]))
                num_keys = int(tokens[2])
                keys = eval(tokens[3])
                pointers = eval(tokens[4])
                pairs = []
                for i in range(num_keys):
                    if len(pointers)-1 >= i:
                        pairs.append([keys[i], pointers[i]])
                    else:
                        pairs.append([keys[i], None])
                
                if len(pointers) > num_keys:
                    rightmost = pointers[-1]
                else:
                    rightmost = None

                new_node = Node(degree, is_leaf, node_id, num_keys, pairs, rightmost)
                nodes.append(new_node)
                nodes_dict[node_id] = new_node
    
    # convert pointer to node object
    for node in nodes:
        p_pairs = []

        if not node.get_is_leaf():      # for non-leaf node
            for k, p in node.get_pairs():
                pointer = None
                if isinstance(p, int):
                    pointer = nodes_dict[p]
                    p_pairs.append([k, pointer])
                else:
                    pointer = p
                    p_pairs.append([k, pointer])
                # set parent
                pointer.set_parent(node)
            node.set_pairs(p_pairs)

        org_rightmost = node.get_rightmost()
        if isinstance(org_rightmost, int):
            node.set_rightmost(nodes_dict[org_rightmost])
            if not node.get_is_leaf():       
                # set parent 
                node.get_rightmost().set_parent(node)
            else:
                node.get_rightmost().set_left_sibling(node)



    root_id = meta_data["root"]
    if len(nodes_dict) > 0:
        root_node = nodes_dict[root_id]
    next_id +=1
        
    return meta_data, root_node, next_id
                

                    

def parse_csv_file(data_file="data.csv"):
    pairs = []
    with open(data_file, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            pairs.append([int(e) for e in line])
        
    return pairs

def save_nodes_to_index_file(index_file="index.dat", root=Node(), degree=0):
    if root is None:
        new_index_file(index_file, degree) # type: ignore
        return
    
    node_queue = deque()
    nodes = set()
    node_data_str = []

    add_str = False

    node_queue.append(root)

    while node_queue:
        node = node_queue.popleft() # type: Node
        if node not in nodes:
            nodes.add(node)
            add_str = True
        
        # non-leaf node 추가
        if not node.get_is_leaf():
            for k, child in node.get_pairs():
                if child is not None:
                    if child not in nodes:
                        node_queue.append(child)

            child = node.get_rightmost()
            if child is not None:
                if child not in nodes:
                    node_queue.append(child)
        # leaf node 추가
        else:
            right_sibling = node.get_rightmost()
            if right_sibling is not None:
                if right_sibling not in nodes:
                    node_queue.append(right_sibling)
        
        # append the node data string
        if add_str:
            node_id = node.get_id()
            node_type = 1 if node.get_is_leaf() else 0
            num_keys = node.get_num_keys()

            keys = []
            values = []
            if not node.get_is_leaf():
                for k, v in node.get_pairs():
                    keys.append(k)
                    values.append(v.get_id())
            else:
                for k, v in node.get_pairs():
                    keys.append(k)
                    values.append(v)
            rightmost = node.get_rightmost()
            if rightmost is not None:
                values.append(rightmost.get_id())

            keys_str = str(keys)
            values_str = str(values)

            line = f"{node_id}, {node_type}, {num_keys}, {keys_str}, {values_str}\n"
            node_data_str.append(line)
            add_str = False

    # print(f"Total Node Nums: {len(nodes)}\n")
    # index file에 meta data와 node data 작성
    with open(index_file, 'w', encoding="utf-8") as f:
        f.write('@ Meta info.\n')
        f.write(f'degree={degree}\n')
        f.write(f'root={root.get_id()}\n')
        f.write(f'nodes_num={len(nodes)}\n')
        f.write('\n')
        f.write('@ Node info.\n')
        f.write('# Node ID, Type (0: non-leaf, 1: leaf), Key Count, [Keys], [Child Node Pointers or Values]\n')

        for line in node_data_str:
            f.write(line)
                
