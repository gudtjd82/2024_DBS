import random
import csv

def generate_random_pairs_csv(input_num_pairs, delete_num_pairs, key_range=(1, 100), value_range=(1000, 1000000), input_file="input_test.csv", delete_file="delete_test.csv"):
    pairs = []
    delete_keys = []
    keys = set()

    while len(pairs) < input_num_pairs:
        # 랜덤한 key와 value 생성
        key = random.randint(key_range[0], key_range[1])
        value = random.randint(value_range[0], value_range[1])

        if key not in keys:
            pairs.append((key, value))
            keys.add(key)
    
    if delete_num_pairs <= input_num_pairs:
        delete_pairs = random.sample(pairs, delete_num_pairs)
        delete_keys = [pair[0] for pair in delete_pairs]
    
    with open(input_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(pairs)
    
    with open(delete_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for key in delete_keys:
            writer.writerow([key])

if __name__ == "__main__":
    input_num_pairs = 20
    delete_num_pairs = 5
    key_range = (1, input_num_pairs*5)
    value_range = (1000, 10000000)
    input_file = "input_test.csv"
    delete_file = "delete_test.csv"

    generate_random_pairs_csv(input_num_pairs, delete_num_pairs, key_range, value_range, input_file, delete_file)