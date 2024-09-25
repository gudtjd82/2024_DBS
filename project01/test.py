from utils import *
from bptree import *
from generate_data_file import *

create_index_file(file_name="index_test.dat", degree=4)

meta_data, root, next_id = parse_index_file(index_file="index_test.dat")
# print(meta_data)
# print(next_id)
# print_tree(root)

# input_num_pairs = 20
# delete_num_pairs = 5
# key_range = (1, input_num_pairs*5)
# value_range = (1000, 10000000)
# input_file = "input_test.csv"
# delete_file = "delete_test.csv"
# generate_random_pairs_csv(input_num_pairs, delete_num_pairs, key_range, value_range, input_file, delete_file)

root = insert(index_file="index_test.dat", input_file="input_test.csv")
if root is None:
    print("Error: root is None")
    exit()

# total_nodes_num = print_tree(root)

# print(f"Total Nodes Num: {total_nodes_num}")
print_tree(root)
print(is_bptree(root, meta_data["degree"]))

# meta_data, root, next_id = parse_index_file(index_file="index_test.dat")


# search_single(index_file="index_test.dat", key=17)
# search_range(index_file="index_test.dat", start_key=0, end_key=100)
