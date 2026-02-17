import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('database/tempest_keep_db.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# 查看有多个 statType 的物品，并显示他们的描述
print('查看物品属性示例:')
count = 0
for item_id, item in items.items():
    # 只看有多个 statType 的物品
    stats = []
    for i in range(1, 8):
        st = item.get(f'statType{i}')
        sv = item.get(f'statValue{i}')
        if st and sv and sv > 0:
            stats.append((st, sv))
    
    if len(stats) >= 2 and count < 20:
        print(f'\n【物品ID: {item_id}】{item.get("nameCn", item.get("name"))}')
        spell_info = item.get('itemSpellsStr', '')
        if spell_info:
            print(f'  效果: {spell_info[:120]}...')
        print(f'  属性:')
        for st, sv in stats:
            print(f'    statType {st}: +{sv}')
        count += 1

print('\n\n建立statType映射:')
print('根据的规律:')
print('- item 32267: statType1=4(+85), statType2=7(+111) -> +85力量, +111耐力')
print('- statType 4 = 力量 (Strength)')
print('- statType 7 = 耐力 (Stamina)')
