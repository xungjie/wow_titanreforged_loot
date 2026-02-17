#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从Altasloot Lua文件中提取所有BOSS官方翻译
数据来源: Altasloot\AtlasLootMY_DungeonsAndRaids\Locales\constants.cn.lua
"""

import re
import json

def extract_boss_translations():
    """从Lua本地化文件中提取BOSS翻译"""
    
    # 读取AtlasLootMY_DungeonsAndRaids的中文本地化文件
    locale_files = [
        'Altasloot/AtlasLootMY_DungeonsAndRaids/Locales/constants.cn.lua',
        'Altasloot/AtlasLootMY/Locales/constants.cn.lua'
    ]
    
    cn_translations = {}
    
    for locale_file in locale_files:
        try:
            with open(locale_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析格式: AL["Boss Name"] = "中文翻译"
            pattern = r'AL\["([^"]+)"\]\s*=\s*"([^"]+)"'
            
            for match in re.finditer(pattern, content):
                en_name = match.group(1)
                zh_name = match.group(2)
                cn_translations[en_name] = zh_name
        except:
            pass
    
    print('=' * 70)
    print('【从Altasloot官方本地化文件提取的BOSS翻译】')
    print('=' * 70)
    print(f'\n总翻译数: {len(cn_translations)}')
    
    # 需要的BOSS列表（从Lua data文件中提取）
    raids = {
        'MoltenCore': {
            'bosses': ['Lucifron', 'Taurajon', 'Gehennas', 'Shazzrah', 'Baron Geddon', 
                       'Sulfuron Harbinger', 'Golemagg the Incinerator', 'Majordomo Executus', 'Ragnaros'],
            'name_en': 'Molten Core',
            'name_zh': '熔火之心'
        },
        'SerpentshrineCavern': {
            'bosses': ['Hydross the Unstable', 'The Lurker Below', 'Leotheras the Blind',
                       'Fathom-Lord Karathress', 'Morogrim Tidewalker', 'Lady Vashj'],
            'name_en': 'Serpentshrine Cavern',
            'name_zh': '毒蛇神殿'
        },
        'TempestKeep': {
            'bosses': ['Alar the Eversoaring', 'Void Reaver', 'Solarian', "Kael'thas Sunstrider"],
            'name_en': 'The Eye',
            'name_zh': '风暴风眼'
        },
        'NaxxramasWrath': {
            'bosses': ['Anub\'Rekhan', 'Grand Widow Faerlina', 'Maexxna',
                      'Noth the Plaguebringer', 'Heigan the Unclean', 'Loatheb',
                      'Patchwerk', 'Grobbulus', 'Gluth', 'Thaddius',
                      'Sapphiron', 'Blood Prince Council', 'Kel\'Thuzad'],
            'name_en': 'Naxxramas',
            'name_zh': '冰冠堡垒'
        },
        'ObsidianSanctum': {
            'bosses': ['Sartharion', 'Tenebron', 'Shadron', 'Vesperon'],
            'name_en': 'The Obsidian Sanctum',
            'name_zh': '黑曜石圣殿'
        },
        'TheEyeOfEternity': {
            'bosses': ['Malygos'],
            'name_en': 'The Eye of Eternity',
            'name_zh': '永恒之眼'
        }
    }
    
    print('\n【BOSS翻译对照表】')
    print('=' * 70)
    
    missing_translations = []
    boss_mapping = {}
    
    for raid_name, raid_info in raids.items():
        boss_list = raid_info['bosses']
        print(f'\n## {raid_name} ({raid_info["name_en"]} / {raid_info["name_zh"]})')
        
        boss_mapping[raid_name] = []
        
        for idx, en_boss in enumerate(boss_list, 1):
            cn_trans = cn_translations.get(en_boss, en_boss)
            
            status = '✓' if en_boss in cn_translations else '✗'
            print(f'  {status} #{idx:2d} {en_boss:40} -> {cn_trans}')
            
            boss_mapping[raid_name].append({
                'id': idx,
                'name_en': en_boss,
                'name_zh': cn_trans
            })
            
            if en_boss not in cn_translations:
                missing_translations.append((raid_name, en_boss))
    
    if missing_translations:
        print(f'\n【缺失的翻译 ({len(missing_translations)}个)】')
        print('=' * 70)
        for raid, boss in missing_translations:
            print(f'  - {raid}: {boss}')
    
    # 保存为JSON格式便于使用
    output = {}
    for raid_name, raid_info in raids.items():
        output[raid_name] = {
            'id': list(raids.keys()).index(raid_name) + 1,
            'name_en': raid_info['name_en'],
            'name_zh': raid_info['name_zh'],
            'bosses': boss_mapping[raid_name]
        }
    
    print(f'\n【统计】')
    print('=' * 70)
    total_bosses = sum(len(re['bosses']) for re in output.values())
    translated_bosses = sum(1 for _ in missing_translations for _ in [1])
    print(f'副本总数: {len(output)}')
    print(f'BOSS总数: {total_bosses}')
    print(f'已翻译: {total_bosses - len(missing_translations)}')
    print(f'缺失: {len(missing_translations)}')
    
    return output, cn_translations

if __name__ == '__main__':
    boss_mapping, all_trans = extract_boss_translations()
