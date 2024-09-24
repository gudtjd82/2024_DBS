from utils import *
from bptree import *
import re

meta_data, root, next_id = parse_index_file("index.dat")
# print(meta_data)
# print(next_id)
print_tree(root)

root = insert(index_file="index.dat", input_file="input.csv")
if root is None:
    print("Error: root is None")
    exit()

print_tree(root)