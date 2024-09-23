from utils import *
from bptree import *
import re

meta_data, root, next_id = parse_index_file("ex_index2.dat")
# print(meta_data)
# print(next_id)
print_tree(root)

insert(index_file="ex_index2.dat", input_file="input.csv")
