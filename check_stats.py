import json

with open('database/tempest_keep_db.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# 搜索所有键
all_keys = set()
for item in list(items.values())[:500]:
    all_keys.update(item.keys())

# 查找统计相关的键
stat_keys = sorted([k for k in all_keys if any(word in k.lower() for word in ['sta', 'str', 'agi', 'int', 'spi', 'crit', 'hit', 'haste', 'sp', 'ap'])])
print("Stat-related keys:", stat_keys)

# 找几个有属性的物品
print("\n搜索有属性的物品:")
count = 0
for item_id, item in items.items():
    # 检查是否有属性大于0
    item_stats = {}
    for key in all_keys:
        val = item.get(key, 0)
        if isinstance(val, (int, float)) and val > 0:
            if any(x in key.lower() for x in ['str', 'agi', 'sta', 'int', 'spi', 'hit', 'crit', 'haste', 'ap', 'sp']):
                item_stats[key] = val
    
    if item_stats and count < 10:
        print(f"\nID: {item_id}, 名字: {item.get('nameCn', item.get('name'))}")
        for k, v in sorted(item_stats.items()):
            print(f"  {k}: {v}")
        count += 1
        
    if count >= 10:
        break
