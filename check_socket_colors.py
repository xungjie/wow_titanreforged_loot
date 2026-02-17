import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('database/tempest_keep_db.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

# 扫描所有socketColor值
socket_colors = {}
for item_id, item in items.items():
    for i in range(1, 4):
        color = item.get(f'socketColor{i}')
        if color:
            if color not in socket_colors:
                socket_colors[color] = []
            socket_colors[color].append(item_id)

print('所有socket颜色代码出现次数:')
for color in sorted(socket_colors.keys()):
    print(f'  Color Code {color}: {len(socket_colors[color])} 次')
    
# 根据WoW标准插槽颜色
print('\nWoW标准插槽颜色映射:')
print('  红色 = 1')
print('  黄色 = 2')
print('  蓝色 = 4')  
print('  紫色/元素 = 8')
print('  绿色 = 16')
print('  棕色 = 32')
print('  透明 = 64')
print('\n实际数据中的映射:')
for color in sorted(socket_colors.keys()):
    mapping = {1: '红色', 2: '黄色', 4: '蓝色', 8: '紫色/元素', 16: '绿色', 32: '棕色', 64: '透明'}
    name = mapping.get(color, f'未知({color})')
    print(f'  socketColor {color} = {name}')
