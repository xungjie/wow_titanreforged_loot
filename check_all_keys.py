import json

with open('database/tempest_keep_db.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# 获取所有键
all_keys = set()
for item in list(items.values())[:1000]:
    all_keys.update(item.keys())

# 打印所有键
print('所有数据库键:')
for key in sorted(all_keys):
    print(f'  {key}')

# 查找有基础属性的物品
print('\n\n查找包含基础属性信息的物品(前5个):')
count = 0
for item_id, item in items.items():
    has_attr = any(item.get(k, 0) > 0 for k in ['druidApAdd'])
    if has_attr and count < 5:
        print(f"\nID: {item_id}, 名字: {item.get('nameCn')}")
        for k in ['druidApAdd', 'statType1', 'statValue1', 'statType2', 'statValue2', 'statType3', 'statValue3']:
            print(f"  {k}: {item.get(k)}")
        count += 1
