#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import json

def analyze_lua_p3_content():
    """Analyze how many items exist for P3 raids in Lua files"""
    
    lua_file = 'Altasloot/AtlasLootMY_DungeonsAndRaids/data-wrath.lua'
    with open(lua_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    p3_raids = {
        'NaxxramasWrath': False,
        'ObsidianSanctum': False,
        'TheEyeOfEternity': False
    }
    
    raid_items = {}
    
    for raid_name in p3_raids.keys():
        # Find the data["RaidName"] = { ... } block
        pattern = rf'data\["{raid_name}"\]\s*=\s*\{{.*?(?=data\["|$)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            raid_block = match.group(0)
            
            # Count item entries: lines like { 1, 39719 }
            item_pattern = r'\{\s*\d+\s*,\s*(\d+)\s*\}'
            items = re.findall(item_pattern, raid_block)
            
            raid_items[raid_name] = len(items)
            p3_raids[raid_name] = True
            
            print(f'✓ {raid_name}: {len(items)} 个物品')
            if len(items) > 0:
                print(f'  样本物品ID: {items[:3]}...')
        else:
            raid_items[raid_name] = 0
            print(f'✗ {raid_name}: 未找到')
    
    print(f'\n总计: {sum(raid_items.values())} 个P3物品')
    
    # Now check if these items are in the current database
    with open('data/items.json', 'r', encoding='utf-8') as f:
        items_db = json.load(f)
    
    print(f'\n当前 items.json: {len(items_db)} 个物品')
    
    # Sample: check if first items from each raid are in database
    for raid_name, item_count in raid_items.items():
        if item_count > 0:
            pattern = rf'data\["{raid_name}"\]\s*=\s*\{{.*?(?=data\["|$)'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                raid_block = match.group(0)
                item_pattern = r'\{\s*\d+\s*,\s*(\d+)\s*\}'
                items = re.findall(item_pattern, raid_block)
                
                sample_item = items[0] if items else None
                if sample_item:
                    in_db = sample_item in items_db
                    status = '✓' if in_db else '✗'
                    print(f'{status} {raid_name} 样本 {sample_item} 在数据库: {in_db}')

if __name__ == '__main__':
    analyze_lua_p3_content()
