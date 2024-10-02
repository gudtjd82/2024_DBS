from utils import *
from bptree import *
from generate_data_file import *
import time

generating = False
inserting = False
deleting = True

printing_tree = True
insertion_debug = False
deletion_debug = True
check_bptree = True


if generating:
    create_index_file(file_name="index_test.dat", degree=4)

    input_num_pairs = 30
    delete_num_pairs = 10
    key_range = (1, input_num_pairs*5)
    value_range = (1000, 10000000)
    input_file = "input_test.csv"
    delete_file = "delete_test.csv"

    print("Generating test data...")
    generate_random_pairs_csv(input_num_pairs, delete_num_pairs, key_range, value_range, input_file, delete_file)
    # print("Data generation completed successfully!")

if inserting:
    # root, next_id = insertion(index_file="index_test.dat", input_file="input2.csv")
    start_time = time.time()
    root, next_id = insertion(index_file="index_test.dat", input_file="input_test.csv", debug=insertion_debug)
    if root is None:
        print("Error: Insertion - root is None")
        exit()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"insertion 수행 시간: {execution_time:.4f}초")


if printing_tree:
    meta_data, root, next_id = parse_index_file(index_file="index_test.dat")
    total_nodes_num = print_tree(root)
    print(f"Total nodes num: {total_nodes_num}")

# print(f"Total Nodes Num: {total_nodes_num}")
if check_bptree and inserting:
    print(is_bptree(root, root.get_degree()))

if deleting:
    start_time = time.time()
    root, next_id = deletetion(index_file="index_test.dat", delete_file="delete_test.csv",debug=deletion_debug)

    if root is None:
        print("Error: Deletion - root is None")
        exit()

    if printing_tree:
        total_nodes_num = print_tree(root)
        print(f"Total nodes num: {total_nodes_num}")
    
    if check_bptree:
        print(is_bptree(root, root.get_degree()))
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"deletion 수행 시간: {execution_time:.4f}초")

# meta_data, root, next_id = parse_index_file(index_file="index_test.dat")


# search_single(index_file="index_test.dat", key=71)
# search_range(index_file="index_test.dat", start_key=8, end_key=35)
