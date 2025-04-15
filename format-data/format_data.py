import os
import pandas as pd
from collections import defaultdict


# @TODO Nie działa dokładnie tak jak ma być poprwaię później
# Define file paths
input_file = 'yoochoose-clicks.dat'
output_dir = 'preprocessed_yoochoose'
os.makedirs(output_dir, exist_ok=True)

# Load the dataset
print("Loading data...")
df = pd.read_csv(input_file, header=None, names=['SessionID', 'Timestamp', 'ItemID', 'Category'])

# Sort by SessionID and Timestamp
df.sort_values(by=['SessionID', 'Timestamp'], inplace=True)

# Group by SessionID and collect ItemIDs
print("Processing sessions...")
session_item_map = df.groupby('SessionID')['ItemID'].apply(list)

# Filter out sessions with less than 2 items
session_item_map = session_item_map[session_item_map.apply(len) >= 2]

# Map ItemIDs to a continuous range starting from 1
item_id_map = {}
item_counter = 1

def map_item_ids(item_list):
    global item_counter
    mapped_list = []
    for item in item_list:
        if item not in item_id_map:
            item_id_map[item] = item_counter
            item_counter += 1
        mapped_list.append(item_id_map[item])
    return mapped_list

# Apply the mapping
print("Mapping item IDs...")
session_item_map = session_item_map.apply(map_item_ids)

# Split into training and test sets
print("Splitting into training and test sets...")
train_sequences = []
test_sequences = []

for session_id, items in session_item_map.items():
    train_sequences.append(items[:-1])
    test_sequences.append(items[-1:])

# Save the processed data
print("Saving processed data...")
with open(os.path.join(output_dir, 'train.txt'), 'w') as f_train, \
     open(os.path.join(output_dir, 'test.txt'), 'w') as f_test:
    for train_seq in train_sequences:
        f_train.write(' '.join(map(str, train_seq)) + '\n')
    for test_seq in test_sequences:
        f_test.write(' '.join(map(str, test_seq)) + '\n')

# Save the item ID mapping
with open(os.path.join(output_dir, 'item_mapping.txt'), 'w') as f_map:
    for original_id, mapped_id in item_id_map.items():
        f_map.write(f"{original_id} {mapped_id}\n")

print(f"Preprocessing complete. Files saved in '{output_dir}' directory.")
