from utils import *
from bptree import *
import re

meta_data, root = parse_index_file("ex_index.dat")
print(meta_data)
print(root)
print()
draw_tree(root)