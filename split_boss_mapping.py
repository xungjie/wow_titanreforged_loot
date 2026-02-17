#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to split boss_mapping.json into per-raid JSON files for optimization.
This allows loading only the boss data for needed raids instead of all at once.

Usage: python split_boss_mapping.py
Output: database/bosses/[raidname].json
"""

import json
import os

def split_boss_mapping():
    """Split the unified boss_mapping.json into per-raid JSON files"""
    
    # Load the unified boss mapping
    with open('database/boss_mapping.json', 'r', encoding='utf-8') as f:
        boss_mapping = json.load(f)
    
    # Create bosses directory if it doesn't exist
    bosses_dir = 'database/bosses'
    os.makedirs(bosses_dir, exist_ok=True)
    
    print('【分割BOSS映射到单个副本文件】')
    print('=' * 60)
    
    raid_files = {}
    
    # Split each raid into its own file
    for raid_name, raid_data in boss_mapping.items():
        file_path = os.path.join(bosses_dir, f'{raid_name}.json')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(raid_data, f, ensure_ascii=False, indent=2)
        
        raid_files[raid_name] = f'{raid_name}.json'
        boss_count = len(raid_data.get('bosses', []))
        file_size = os.path.getsize(file_path)
        
        print(f'✓ {raid_name}: {boss_count} bosses -> {file_size:,} bytes')
    
    # Create an index file for easy reference
    index_file = os.path.join(bosses_dir, 'index.json')
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump({
            'raids': list(raid_files.keys()),
            'files': raid_files,
            'total_bosses': sum(len(v.get('bosses', [])) for v in boss_mapping.values()),
            'total_raids': len(boss_mapping)
        }, f, ensure_ascii=False, indent=2)
    
    print(f'\n✓ Index file created: {index_file}')
    print('\n【优化建议】')
    print('=' * 60)
    print('在 index.html 中，可以改进为：')
    print('1. 加载副本选择器列表只需加载 bosses/index.json')
    print('2. 当用户选择副本时，动态加载对应的 bosses/[raidname].json')
    print('3. 这样可以大幅减少初始加载时间')
    print('\n示例代码：')
    print('''
// 加载BOSS映射数据（仅加载所需副本）
async function loadBossMapping(raidName) {
  try {
    const url = raidName 
      ? `database/bosses/${raidName}.json`
      : 'database/boss_mapping.json'; // 加载所有
    const response = await fetch(url);
    if (response.ok) {
      const data = await response.json();
      bossMappingData = data;
      console.log(`✅ Loaded boss mapping for ${raidName || 'all raids'}`);
      return true;
    }
  } catch (e) {
    console.warn('Failed to load boss mapping:', e);
  }
  return false;
}
    ''')

if __name__ == '__main__':
    split_boss_mapping()
