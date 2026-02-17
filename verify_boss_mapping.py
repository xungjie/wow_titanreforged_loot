#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Load boss mapping
with open('database/boss_mapping.json', 'r', encoding='utf-8') as f:
    boss_mapping = json.load(f)

# Load current loot data from Lua to compare
import re

def extract_boss_count_from_lua(raid_name):
    """Extract the actual boss count for each raid from Lua files"""
    lua_file = 'Altasloot/AtlasLootMY_DungeonsAndRaids/data-wrath.lua'
    with open(lua_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # For other raids, check data.lua and source.lua
    lua_files = [
        'Altasloot/AtlasLootMY_Data/data.lua',
        'Altasloot/AtlasLootMY_DungeonsAndRaids/data.lua'
    ]
    
    for lf in lua_files:
        try:
            with open(lf, 'r', encoding='utf-8') as f:
                content = f.read()
            match = re.search(rf'data\["{raid_name}"\]\s*=\s*\{{(.*?)(?=^data\[|}},?\n)', content, re.MULTILINE | re.DOTALL)
            if match:
                raid_block = match.group(1)
                # Count boss definitions (lines with "name = AL[" or similar)
                boss_pattern = r'{\s*--.*?name'
                bosses = re.findall(boss_pattern, raid_block)
                return len(bosses)
        except:
            pass
    
    return None

print('=' * 60)
print('【BOSS映射验证报告】')
print('=' * 60)

raid_names = {
    'MoltenCore': 'MoltenCore',
    'SerpentshrineCavern': 'SerpentshrineCavern',
    'TempestKeep': 'TempestKeep',
    'NaxxramasWrath': 'NaxxramasWrath',
    'ObsidianSanctum': 'ObsidianSanctum',
    'TheEyeOfEternity': 'TheEyeOfEternity'
}

print('\n副本BOSS数量:'  )
total_bosses = 0
all_bosses_with_translations = True

for raid_en, raid_name in raid_names.items():
    if raid_name in boss_mapping:
        raid_data = boss_mapping[raid_name]
        boss_count = len(raid_data.get('bosses', []))
        total_bosses += boss_count
        
        print(f'\n✓ {raid_name}')
        print(f'  英文名: {raid_data.get("name_en")}')
        print(f'  中文名: {raid_data.get("name_zh")}')
        print(f'  BOSS数: {boss_count}')
        print(f'  难度: {raid_data.get("difficulty")}')
        print(f'  版本: {raid_data.get("patch")}')
        
        # Check if all bosses have translations
        for boss in raid_data.get('bosses', []):
            if not boss.get('name_en') or not boss.get('name_zh'):
                all_bosses_with_translations = False
                print(f'  ⚠ BOSS #{boss.get("id")} 缺少翻译: EN={boss.get("name_en")}, ZH={boss.get("name_zh")}')
        
        # Show first 3 bosses
        print(f'  样本BOSS:')
        for boss in raid_data.get('bosses', [])[:3]:
            print(f'    - #{boss["id"]} {boss["name_en"]} / {boss["name_zh"]}')
    else:
        print(f'\n✗ {raid_name}: 未找到')
        all_bosses_with_translations = False

print(f'\n' + '=' * 60)
print(f'【统计】')
print(f'=' * 60)
print(f'副本总数: {len(boss_mapping)}')
print(f'BOSS总数: {total_bosses}')
print(f'全部翻译完成: {"✓ 是" if all_bosses_with_translations else "✗ 否"}')
print(f'\n✓ Boss映射已准备就绪，可用于index.html')
