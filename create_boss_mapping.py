#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import json

def extract_boss_data_from_lua():
    """Extract boss information from Lua files"""
    
    boss_data = {
        "1": {  # MoltenCore
            "name_en": "Molten Core",
            "name_zh": "熔火之心",
            "zone_id": 409,
            "difficulty": "Raid 40",
            "phase": 1,
            "bosses": {}
        },
        "2": {  # SerpentshrineCavern
            "name_en": "Serpentshrine Cavern",
            "name_zh": "毒蛇神殿",
            "zone_id": 717,
            "difficulty": "Raid 25",
            "phase": 2,
            "bosses": {}
        },
        "3": {  # TempestKeep
            "name_en": "The Eye",
            "name_zh": "风暴风眼",
            "zone_id": 564,
            "difficulty": "Raid 25",
            "phase": 2,
            "bosses": {}
        },
        "4": {  # NaxxramasWrath
            "name_en": "Naxxramas",
            "name_zh": "冰冠堡垒之战 - 奥杜尔",
            "zone_id": 3456,
            "difficulty": "Raid 10/25",
            "phase": 3,
            "bosses": {}
        },
        "5": {  # ObsidianSanctum
            "name_en": "The Obsidian Sanctum",
            "name_zh": "黑曜石圣殿",
            "zone_id": 615,
            "difficulty": "Raid 10/25",
            "phase": 3,
            "bosses": {}
        },
        "6": {  # TheEyeOfEternity
            "name_en": "The Eye of Eternity",
            "name_zh": "永恒之眼",
            "zone_id": 616,
            "difficulty": "Raid 10/25",
            "phase": 3,
            "bosses": {}
        }
    }
    
    # Parse bosses from data-wrath.lua
    lua_file = 'Altasloot/AtlasLootMY_DungeonsAndRaids/data-wrath.lua'
    with open(lua_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    raid_mappings = {
        'NaxxramasWrath': '4',
        'ObsidianSanctum': '5',
        'TheEyeOfEternity': '6'
    }
    
    for raid_lua_name, raid_id in raid_mappings.items():
        # Extract raid block
        pattern = rf'data\["{raid_lua_name}"\]\s*=\s*\{{(.*?)(?=data\[|$)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            raid_block = match.group(1)
            
            # Find boss entries: { -- Comment with boss name
            boss_pattern = r'\{\s*--\s*([A-Z][^}]*?)\s*(npcID|name)\s*=\s*([^,\n]*)'
            boss_matches = re.finditer(boss_pattern, raid_block)
            
            boss_num = 1
            for bm in boss_matches:
                boss_name_raw = bm.group(1).strip()
                # Clean up boss name
                boss_name = re.sub(r'^\w+', '', boss_name_raw).strip()
                if not boss_name:
                    boss_name = boss_name_raw
                
                boss_data[raid_id]['bosses'][str(boss_num)] = {
                    "name_en": boss_name,
                    "name_zh": boss_name,  # Will update manually or later
                    "npc_id": None
                }
                boss_num += 1
    
    return boss_data

# Hard-coded boss mappings based on WoW knowledge
boss_mapping = {
    "MoltenCore": {
        "id": "1",
        "name_en": "Molten Core",
        "name_zh": "熔火之心",
        "zone_id": 409,
        "difficulty": "40-Player Raid",
        "phase": 1,
        "patch": "1.8",
        "bosses": [
            {"id": 1, "name_en": "Lucifron", "name_zh": "露西弗伦"},
            {"id": 2, "name_en": "Taurajon", "name_zh": "陶拉焦恩"},
            {"id": 3, "name_en": "Gehennas", "name_zh": "盖赫纳斯"},
            {"id": 4, "name_en": "Shazzrah", "name_zh": "沙兹拉赫"},
            {"id": 5, "name_en": "Baron Geddon", "name_zh": "盖顿男爵"},
            {"id": 6, "name_en": "Sulfuron Harbinger", "name_zh": "硫磺顿先驱者"},
            {"id": 7, "name_en": "Golemagg the Incinerator", "name_zh": "焚火傀儡"},
            {"id": 8, "name_en": "Majordomo Executus", "name_zh": "管家埃克苏图斯"},
            {"id": 9, "name_en": "Ragnaros", "name_zh": "拉格纳罗斯"}
        ]
    },
    "SerpentshrineCavern": {
        "id": "2",
        "name_en": "Serpentshrine Cavern",
        "name_zh": "毒蛇神殿",
        "zone_id": 717,
        "difficulty": "25-Player Raid",
        "phase": 2,
        "patch": "2.1",
        "bosses": [
            {"id": 1, "name_en": "Hydross the Unstable", "name_zh": "不稳定的海德罗斯"},
            {"id": 2, "name_en": "The Lurker Below", "name_zh": "深潜者"},
            {"id": 3, "name_en": "Leotheras the Blind", "name_zh": "盲眼莱欧塞拉斯"},
            {"id": 4, "name_en": "Fathom-Lord Karathress", "name_zh": "深洋领主卡拉瑟斯"},
            {"id": 5, "name_en": "Morogrim Tidewalker", "name_zh": "摩罗格瑞姆潮行者"},
            {"id": 6, "name_en": "Lady Vashj", "name_zh": "瓦丝琪夫人"}
        ]
    },
    "TempestKeep": {
        "id": "3",
        "name_en": "The Eye",
        "name_zh": "风暴风眼",
        "zone_id": 564,
        "difficulty": "25-Player Raid",
        "phase": 2,
        "patch": "2.1",
        "bosses": [
            {"id": 1, "name_en": "Alar the Eversoaring", "name_zh": "永翔的艾拉尔"},
            {"id": 2, "name_en": "Void Reaver", "name_zh": "虚空掠夺者"},
            {"id": 3, "name_en": "Solarian", "name_zh": "索拉瑞恩"},
            {"id": 4, "name_en": "Kael'thas Sunstrider", "name_zh": "凯尔萨斯·阳羽"}
        ]
    },
    "NaxxramasWrath": {
        "id": "4",
        "name_en": "Naxxramas",
        "name_zh": "冰冠堡垒之战 - 奥杜尔",
        "zone_id": 3456,
        "difficulty": "10/25-Player Raid",
        "phase": 3,
        "patch": "3.0",
        "bosses": [
            # Arachnid Quarter
            {"id": 1, "name_en": "Anub'Rekhan", "name_zh": "阿努布雷克汗", "quarter": "Arachnid Quarter"},
            {"id": 2, "name_en": "Grand Widow Faerlina", "name_zh": "大寡妇法琳娜", "quarter": "Arachnid Quarter"},
            {"id": 3, "name_en": "Maexxna", "name_zh": "玛克丝娜", "quarter": "Arachnid Quarter"},
            # Plague Quarter
            {"id": 4, "name_en": "Noth the Plaguebringer", "name_zh": "瘟疫使者诺斯", "quarter": "Plague Quarter"},
            {"id": 5, "name_en": "Heigan the Unclean", "name_zh": "污秽的海根", "quarter": "Plague Quarter"},
            {"id": 6, "name_en": "Loatheb", "name_zh": "厌恶之心", "quarter": "Plague Quarter"},
            # Frost Wing
            {"id": 7, "name_en": "Sapphiron", "name_zh": "蓝宝石", "quarter": "Frost Wing"},
            # Construct Quarter
            {"id": 8, "name_en": "Patchwerk", "name_zh": "缝合怪", "quarter": "Construct Quarter"},
            {"id": 9, "name_en": "Grobbulus", "name_zh": "葛罗布鲁斯", "quarter": "Construct Quarter"},
            {"id": 10, "name_en": "Gluth", "name_zh": "格鲁斯", "quarter": "Construct Quarter"},
            {"id": 11, "name_en": "Thaddius", "name_zh": "撒迪乌斯", "quarter": "Construct Quarter"},
            # Arachnid Quarter continued
            {"id": 12, "name_en": "Blood Prince Council", "name_zh": "血王子议会", "quarter": "Blood Wing"},
            # Final boss
            {"id": 13, "name_en": "Kel'Thuzad", "name_zh": "克尔苏加德"}
        ]
    },
    "ObsidianSanctum": {
        "id": "5",
        "name_en": "The Obsidian Sanctum",
        "name_zh": "黑曜石圣殿",
        "zone_id": 615,
        "difficulty": "10/25-Player Raid",
        "phase": 3,
        "patch": "3.0",
        "bosses": [
            {"id": 1, "name_en": "Sartharion the Onyx Dragon", "name_zh": "玛瑞苟斯（黑龙之王）"},
            {"id": 2, "name_en": "Tenebron", "name_zh": "坦尼布龙"},
            {"id": 3, "name_en": "Shadron", "name_zh": "沙德龙"},
            {"id": 4, "name_en": "Vesperon", "name_zh": "维斯佩龙"}
        ]
    },
    "TheEyeOfEternity": {
        "id": "6",
        "name_en": "The Eye of Eternity",
        "name_zh": "永恒之眼",
        "zone_id": 616,
        "difficulty": "10/25-Player Raid",
        "phase": 3,
        "patch": "3.0",
        "bosses": [
            {"id": 1, "name_en": "Malygos", "name_zh": "玛里苟斯"}
        ]
    }
}

if __name__ == '__main__':
    # Save to file
    output_file = 'database/boss_mapping.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(boss_mapping, f, ensure_ascii=False, indent=2)
    
    print(f'✓ Boss mapping saved to {output_file}')
    print(f'\n副本总数: {len(boss_mapping)}')
    for raid_name, raid_data in boss_mapping.items():
        boss_count = len(raid_data.get('bosses', []))
        print(f'  - {raid_name}: {boss_count} bosses')
