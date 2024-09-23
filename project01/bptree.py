from node import *
from utils import *

def create_bptree(file_name="index.dat", b=5):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write("@ Meta info.\n")
        file.write("b={}\n".format(b))
        file.write("root=0\n")
        file.write("\n")
        file.write("@ Node info.\n")
        file.write("# Node ID, Type (0: non-leaf, 1: leaf), Key Count, [Keys], [Child Node Pointers or Values]\n")

def insert(index_file="index.dat", input_file="input.csv"):
    new_node = None

    meta_data, root, next_id = parse_index_file(index_file)
    input_pairs = parse_csv_file(input_file)

    degree = meta_data["b"]
    root_id = meta_data["root"]
    for pair in input_pairs:
        # tree가 비어있을 때
        if root_id == 0:
            new_node = Node(True, next_id)
            root_id = next_id
            root = new_node
            next_id +=1
            if new_node.add_pair(pair) < 0:
                print("ERROR: Duplicated key")
                return None
            continue
        
        # tree에 node가 존재할 때
        

    return root
def delete(index_file="index.dat", data_file="delete.csv"):
    print("deletion")
    # todo

def search_single(index_file="index.dat", key=0):
    print("search single key")
    # todo

def search_range(index_file="index.dat", start_key=0, end_key=0):
    print("search keys in range")
    # todo7