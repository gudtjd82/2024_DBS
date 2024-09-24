import random
import csv

def generate_random_pairs_csv(num_pairs, key_range=(1, 100), value_range=(1000, 1000000), file_name="input_test.csv"):
    pairs = []
    keys = set()

    while len(pairs) < num_pairs:
        # 랜덤한 key와 value 생성
        key = random.randint(key_range[0], key_range[1])
        value = random.randint(value_range[0], value_range[1])

        if key not in keys:
            pairs.append((key, value))
            keys.add(key)
    
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(pairs)

if __name__ == "__main__":
    num_pairs = 20
    key_range = (1, 100)
    value_range = (1000, 1000000)
    file_name = "input_test.csv"

    generate_random_pairs_csv(num_pairs, key_range, value_range, file_name)