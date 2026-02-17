import json
import sys

# Set encoding
sys.stdout.reconfigure(encoding='utf-8')

with open('database/tempest_keep_db.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# Get all keys from first 1000 items
all_keys = set()
for item in list(items.values())[:1000]:
    all_keys.update(item.keys())

# Print all keys
print('All database keys:')
for key in sorted(all_keys):
    print(f'  {key}')

# Show a sample item with multiple stat types
print('\n\nSample item with statType and statValue:')
for item_id, item in items.items():
    if item.get('statType1') and item.get('statType2'):
        print(f"ID: {item_id}, Name: {item.get('nameCn')}")
        for i in range(1, 8):
            stat_type = item.get(f'statType{i}')
            stat_value = item.get(f'statValue{i}')
            if stat_type and stat_value:
                print(f"  statType{i}: {stat_type}, statValue{i}: {stat_value}")
        break
