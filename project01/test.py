from utils import *
# from bptree import *
import re

meta_data, root, next_id = parse_index_file("index.dat")
# degree = meta_data["b"]
# print(degree)
print(meta_data)
print(root)
print(next_id)
# print()
print_tree(root)
