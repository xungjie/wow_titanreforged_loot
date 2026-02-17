import json

with open('database/tempest_keep_db.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# Look for items that have stat bonuses in itemSpellsStr or descriptions
print('Looking for items with stat bonuses (strength, agility, stamina, etc):')
count = 0
for item_id, item in items.items():
    spell_str = item.get('itemSpellsStr', '')
    spell_text = item.get('spellText', '')
    combined = (spell_str + ' ' + spell_text).lower()
    
    # Search for Chinese attribute names
    if any(x in combined for x in ['力量', '敏捷', '体力', '耐力', '智力', '精神', '护甲']):
        if count < 10:
            print(f"\n【ID: {item_id}】{item.get('nameCn', item.get('name'))}")
            print(f"  itemSpellsStr: {spell_str}")
            print(f"  spellText: {spell_text}")
            count += 1
        else:
            break

# Also show a general stat file example
print('\n\n="WoW基础属性类型映射示例"')
print('根据常见的WoW数据库，statType可能的含义：')
stat_type_map = {
    3: '暴击等级 (Critical Strike Rating)',
    4: '防御等级 (Defense Rating)',  
    5: '躲闪等级 (Dodge Rating)',
    6: '招架等级 (Parry Rating)',
    7: '格挡值 (Block Value)',
    # 以下是猜测
    'unknown': '数据库中没有直接的力量、敏捷、体力等基础属性字段'
}
for k, v in stat_type_map.items():
    print(f"  {k}: {v}")
