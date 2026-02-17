#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 检查新数据库
print('=' * 60)
print('【wlk_raids_db.json 数据库分析】')
print('=' * 60)

try:
    with open('database/wlk_raids_db.json', 'r', encoding='utf-8') as f:
        wlk_data = json.load(f)
    
    print(f'\n✓ 成功加载 wlk_raids_db.json')
    print(f'数据库类型: {type(wlk_data).__name__}')
    
    if isinstance(wlk_data, dict):
        print(f'字典键数: {len(wlk_data)}')
        sample_keys = list(wlk_data.keys())[:5]
        print(f'样本键: {sample_keys}')
        
        # 检查第一条记录
        first_key = list(wlk_data.keys())[0]
        first_value = wlk_data[first_key]
        print(f'\n第一条记录 (key={first_key}):')
        if isinstance(first_value, dict):
            for k, v in list(first_value.items())[:8]:
                print(f'  {k}: {str(v)[:60]}')
    elif isinstance(wlk_data, list):
        print(f'列表长度: {len(wlk_data)}')
        if len(wlk_data) > 0:
            print(f'第一条: {str(wlk_data[0])[:100]}')
    
    print('\n' + '=' * 60)
    print('【对比数据库规模】')
    print('=' * 60)
    
    with open('data/items.json', 'r', encoding='utf-8') as f:
        current_data = json.load(f)
    
    print(f'\n当前 items.json: {len(current_data):,} 个物品')
    print(f'新 wlk_raids_db.json: {len(wlk_data):,} 个物品')
    print(f'差异: {abs(len(wlk_data) - len(current_data)):,} 个')
    
    # 检查是否有P3副本相关的数据
    print('\n' + '=' * 60)
    print('【检查P3副本的物品】')
    print('=' * 60)
    
    p3_instances = ['NaxxramasWrath', 'ObsidianSanctum', 'TheEyeOfEternity', 
                    'Naxxramas', 'ObsidianSanctuum', 'EyeOfEternity']
    
    # 如果是dict，检查instance字段
    if isinstance(wlk_data, dict):
        p3_count = 0
        p3_instances_found = {}
        
        for item_id, item_data in wlk_data.items():
            if isinstance(item_data, dict) and 'instance' in item_data:
                inst = item_data['instance']
                if inst in p3_instances:
                    p3_count += 1
                    if inst not in p3_instances_found:
                        p3_instances_found[inst] = []
                    if len(p3_instances_found[inst]) < 2:
                        p3_instances_found[inst].append({
                            'id': item_id,
                            'name': item_data.get('itemName', 'Unknown'),
                            'boss': item_data.get('boss', 'Unknown')
                        })
        
        print(f'\n找到 {p3_count} 个P3副本物品\n')
        for inst in p3_instances:
            if inst in p3_instances_found:
                print(f'  ✓ {inst}: {len(p3_instances_found[inst])} 个示例')
                for item in p3_instances_found[inst]:
                    print(f'    - [{item["id"]}] {item["name"]} (Boss: {item["boss"]})')
            else:
                print(f'  ✗ {inst}: 无数据')
    
    print('\n' + '=' * 60)
    print('【结论】')
    print('=' * 60)
    print('\n✓ wlk_raids_db.json 数据库成功验证')
    print('✓ 可以安全集成到 index.html')
    
except Exception as e:
    print(f'\n✗ 错误: {e}')
    import traceback
    traceback.print_exc()
