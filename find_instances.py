import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 查看所有三个源文件中的副本名称
for filename in ['source.lua', 'source-tbc.lua', 'source-wrath.lua']:
    filepath = f'Altasloot/AtlasLootMY_Data/{filename}'
    print(f'\n{filename} 中的副本:')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 搜索 AtlasLootIDs
        match = re.search(r'\["AtlasLootIDs"\]\s*=\s*\{([\s\S]*?)\}', content)
        if match:
            body = match.group(1)
            ids = []
            for m in re.finditer(r'"([^"]+)"', body):
                ids.append(m.group(1))
            
            for i, instance_id in enumerate(ids, 1):
                # 搜索相关关键词
                if any(x in instance_id.lower() for x in ['naxx', 'obsidian', 'eternal', 'eye', 'malygos', 'sapphiron']):
                    print(f'  *** {instance_id}')
                else:
                    print(f'      {instance_id}')
    except Exception as e:
        print(f'  Error: {e}')
