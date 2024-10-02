import sys
import os
from bptree import *

def main():
    if len(sys.argv) < 4:
        print("Invalid command. Usage: python main.py <command> [options]")
        sys.exit(1)

    command = sys.argv[1]
    index_file = sys.argv[2]

    if command == '-c':
        # Creation: python main.py -c index.dat <degree>
        if len(sys.argv) != 4:
            print("Usage: python main.py -c <index_file> <degree>")
            sys.exit(1)
        degree = int(sys.argv[3])
        create_index_file(index_file, degree)
    
    elif command == '-i':
        # Insertion: python main.py -i index.dat <data_file>
        if len(sys.argv) != 4:
            print("Usage: python main.py -i <index_file> <data_file>")
            sys.exit(1)
        input_file = sys.argv[3]
        insertion(index_file, input_file)
    
    elif command == '-d':
        # Deletion: python main.py -d index.dat <data_file>
        if len(sys.argv) != 4:
            print("Usage: python main.py -d <index_file> <data_file>")
            sys.exit(1)
        delete_file = sys.argv[3]
        deletion(index_file, delete_file)
    
    elif command == '-s':
        # Single Key Search: python main.py -s index.dat <key>
        if len(sys.argv) != 4:
            print("Usage: python main.py -s <index_file> <key>")
            sys.exit(1)
        key = int(sys.argv[3])
        search_single(index_file, key)
    
    elif command == '-r':
        # Ranged Search: python main.py -r index.dat <start_key> <end_key>
        if len(sys.argv) != 5:
            print("Usage: python main.py -r <index_file> <start_key> <end_key>")
            sys.exit(1)
        start_key = int(sys.argv[3])
        end_key = int(sys.argv[4])
        search_range(index_file, start_key, end_key)
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: -c, -i, -d, -s, -r")
        sys.exit(1)

if __name__ == "__main__":
    main()