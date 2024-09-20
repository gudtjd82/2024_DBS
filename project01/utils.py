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
    nodes = []
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

                nodes.append(Node(is_leaf, node_id, num_keys, pairs, rightmost))
        
    return meta_data, nodes
                

                    

def parse_csv_file(data_file="data.csv"):
    pairs = []
    with open(data_file, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)

        for line in csv_reader:
            pairs.append([int(e) for e in line])
        
    return pairs