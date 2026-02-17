import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('database/tempest_keep_db.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

item = items.get('29985')
if item:
    print('【物品ID: 29985】')
    print('名称:', item.get('nameCn', item.get('name')))
    print('品质:', item.get('quality'))
    print('物品等级:', item.get('itemLevel'))
    print('装备类型:', item.get('inventoryType'))
    print('itemClass/subClass:', item.get('itemClass'), '/', item.get('subClass'))
    print()
    print('属性信息:')
    for i in range(1, 8):
        st = item.get(f'statType{i}')
        sv = item.get(f'statValue{i}')
        if st:
            print(f'  statType{i}: {st}, statValue{i}: {sv}')
    print()
    print('插槽信息:')
    for i in range(1, 4):
        color = item.get(f'socketColor{i}')
        if color:
            print(f'  socketColor{i}: {color}')
    print()
    print('socket奖励:')
    bonus = item.get('socketBonusStr')
    print('  socketBonusStr:', bonus)
    print()
    print('装备效果:')
    print('  itemSpellsStr:', item.get('itemSpellsStr', ''))
else:
    print('物品不存在')
