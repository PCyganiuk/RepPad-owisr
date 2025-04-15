import argparse

parser = argparse.ArgumentParser(prog = 'dataset_stats')
parser.add_argument('--data_name')
args = parser.parse_args()

file = open(args.data_name, 'r')
lines_list = file.readlines()

user_count = len(lines_list)
items = set()
total_interactions = 0

longest_sequence = 0

for line in lines_list:
    interactions = line.split()[1:]
    total_interactions += len(interactions)
    if len(interactions) > longest_sequence:
        longest_sequence = len(interactions)
    for item in interactions:
        items.add(item)

item_count = len(items)

sparsity = 1 - total_interactions / (longest_sequence * user_count)

print(f'# Users:\t{user_count}')
print(f'# Items:\t{item_count}')
print(f'# Inter:\t{total_interactions}')
print(f'# AvgLen:\t{total_interactions/user_count:.1f}')
print(f'Sparsity:\t{100*sparsity:.2f}%')