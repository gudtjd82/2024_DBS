import csv
import re
from node import *
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
def parse_index_file(index_file="index.dat"):
    # todo
    meta_data = {}
    nodes = []          # 필요 없으면 삭제
    root_node = None
    nodes_dict = {}
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

                is_leaf = bool(int(tokens[1]))
                num_keys = int(tokens[2])
                keys = eval(tokens[3])
                pointers = eval(tokens[4])
                pairs = []
                for i in range(num_keys):
                    if len(pointers)-1 >= i:
                        pairs.append((keys[i], pointers[i]))
                    else:
                        pairs.append((keys[i], None))
                
                if len(pointers) > num_keys:
                    rightmost = pointers[-1]
                else:
                    rightmost = None

                new_node = Node(is_leaf, node_id, num_keys, pairs, rightmost)
                nodes.append(new_node)
                nodes_dict[node_id] = new_node
    
    # convert pointer to node object
    for node in nodes:
        p_pairs = []

        if not node.get_is_leaf():      # for non-leaf node
            for k, p in node.get_pairs():
                if isinstance(p, int):
                    p_pairs.append((k, nodes_dict[p]))
                else:
                    p_pairs.append((k, p))
            node.set_pairs(p_pairs)

        org_rightmost = node.get_rightmost()
        if isinstance(org_rightmost, int):
            node.set_rightmost(nodes_dict[org_rightmost])       

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

def save_nodes(index_file="index.dat", nodes=[Node()]):
    print()
    # todo
    # 바뀐 부분만 저장
