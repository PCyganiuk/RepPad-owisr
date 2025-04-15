import os
import pandas as pd

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

# Save the full sequences in one file (sorted by SessionID)
print("Saving processed data...")
session_item_map = session_item_map.sort_index()

with open(os.path.join(output_dir, 'data.txt'), 'w') as f_out:
    for idx, item_seq in enumerate(session_item_map, start=1):
        f_out.write(f"{idx} " + ' '.join(map(str, item_seq)) + '\n')



# Save the item ID mapping
with open(os.path.join(output_dir, 'item_mapping.txt'), 'w') as f_map:
    for original_id, mapped_id in item_id_map.items():
        f_map.write(f"{original_id} {mapped_id}\n")

print(f"Preprocessing complete. Files saved in '{output_dir}' directory.")
