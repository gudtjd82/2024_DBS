from utils import *
import re

meta_data, nodes = parse_index_file("index.dat")
print(meta_data)
for node in nodes:
    node.print_info()