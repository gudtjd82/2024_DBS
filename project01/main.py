import sys
import os
from bptree import *

def main():
    if len(sys.argv) < 3:
        print("Invalid command. Usage: python bptree.py <command> [options]")
        sys.exit(1)

    command = sys.argv[1]
    index_file = sys.argv[2]

    if command == '-c':
        # Creation: python bptree.py -c index.dat <degree>
        if len(sys.argv) != 4:
            print("Usage: python bptree.py -c <index_file> <degree>")
            sys.exit(1)
        degree = int(sys.argv[3])
        create_index_file(index_file, degree)
    
    elif command == '-i':
        # Insertion: python bptree.py -i index.dat <data_file>
        if len(sys.argv) != 4:
            print("Usage: python bptree.py -i <index_file> <data_file>")
            sys.exit(1)
        data_file = sys.argv[3]
        insert_into_bptree(index_file, data_file)
    
    elif command == '-d':
        # Deletion: python bptree.py -d index.dat <data_file>
        if len(sys.argv) != 4:
            print("Usage: python bptree.py -d <index_file> <data_file>")
            sys.exit(1)
        data_file = sys.argv[3]
        delete_from_bptree(index_file, data_file)
    
    elif command == '-s':
        # Single Key Search: python bptree.py -s index.dat <key>
        if len(sys.argv) != 4:
            print("Usage: python bptree.py -s <index_file> <key>")
            sys.exit(1)
        key = int(sys.argv[3])
        single_search_bptree(index_file, key)
    
    elif command == '-r':
        # Ranged Search: python bptree.py -r index.dat <start_key> <end_key>
        if len(sys.argv) != 5:
            print("Usage: python bptree.py -r <index_file> <start_key> <end_key>")
            sys.exit(1)
        start_key = int(sys.argv[3])
        end_key = int(sys.argv[4])
        ranged_search_bptree(index_file, start_key, end_key)
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: -c, -i, -d, -s, -r")
        sys.exit(1)

if __name__ == "__main__":
    print()