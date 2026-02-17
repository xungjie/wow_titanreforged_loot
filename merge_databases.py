#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Check if wlk_raids_db has the sample P3 items
with open('database/wlk_raids_db.json', 'r', encoding='utf-8') as f:
    wlk_db = json.load(f)

sample_items = ['39719', '40437', '40562']

print('检查 wlk_raids_db.json 中是否包含P3物品:')
for item_id_str in sample_items:
    if item_id_str in wlk_db:
        item = wlk_db[item_id_str]
        print(f'✓ {item_id_str}: {item.get("nameCn", "Unknown")} (quality: {item.get("quality")})')
    else:
        print(f'✗ {item_id_str}: 未找到')

# Now merge both databases (wlk_db as primary, items.json as fallback)
with open('data/items.json', 'r', encoding='utf-8') as f:
    current_db = json.load(f)

print(f'\n当前 items.json: {len(current_db)} 个物品')
print(f'新 wlk_raids_db: {len(wlk_db)} 个物品')

# Check for duplicates
duplicate_count = 0
for item_id in current_db.keys():
    if item_id in wlk_db:
        duplicate_count += 1

print(f'重复项: {duplicate_count} 个')

# Create merged database (wlk takes priority to get P3 items)
merged = {}
merged.update(current_db)  # Add current first
merged.update(wlk_db)       # Then overwrite with wlk (which has P3)

print(f'合并后: {len(merged)} 个物品')
print(f'增加新物品: {len(merged) - len(current_db)} 个')

# Save merged database
output_path = 'database/merged_items_db.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f'\n✓ 已保存合并数据库到: {output_path}')
