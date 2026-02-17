# Boss Mapping 数据库文档

## 概述

本项目包含一个完整的WoW副本BOSS信息数据库，支持多语言（中文/英文），可用于多个平台。

## 文件结构

```
database/
├── boss_mapping.json           # 所有副本BOSS的完整映射（统一文件）
└── bosses/                      # 分割后的按副本存储的BOSS文件（用于优化）
    ├── index.json              # BOSS目录索引
    ├── MoltenCore.json         # 熔火之心 (9个BOSS)
    ├── SerpentshrineCavern.json # 毒蛇神殿 (6个BOSS)
    ├── TempestKeep.json        # 风暴风眼 (4个BOSS)
    ├── NaxxramasWrath.json     # 冰冠堡垒 (13个BOSS)
    ├── ObsidianSanctum.json    # 黑曜石圣殿 (4个BOSS)
    └── TheEyeOfEternity.json   # 永恒之眼 (1个BOSS)
```

## 数据格式

### 完整格式 (boss_mapping.json)

```json
{
  "RaidName": {
    "id": "1",
    "name_en": "English Name",
    "name_zh": "中文名称",
    "zone_id": 409,
    "difficulty": "40-Player Raid",
    "phase": 1,
    "patch": "1.8",
    "bosses": [
      {
        "id": 1,
        "name_en": "Boss Name",
        "name_zh": "BOSS名称",
        "quarter": "Quarter Name"  // 可选，用于分组
      }
    ]
  }
}
```

## 副本列表

| 副本名 | 缩写 | 英文 | BOSS数 | 难度 | 版本 | Phase |
|-------|------|------|--------|------|------|-------|
| 熔火之心 | MC | Molten Core | 9 | 40人 | 1.8 | P1 |
| 毒蛇神殿 | SSC | Serpentshrine Cavern | 6 | 25人 | 2.1 | P2 |
| 风暴风眼 | TK | The Eye | 4 | 25人 | 2.1 | P2 |
| 冰冠堡垒 | Naxx | Naxxramas | 13 | 10/25人 | 3.0 | P3 |
| 黑曜石圣殿 | OS | The Obsidian Sanctum | 4 | 10/25人 | 3.0 | P3 |
| 永恒之眼 | Eye | The Eye of Eternity | 1 | 10/25人 | 3.0 | P3 |

## 使用示例

### JavaScript (前端)

#### 简单加载 - 加载所有BOSS
```javascript
let bossMappingData = {};

async function loadBossMapping() {
  const response = await fetch('database/boss_mapping.json');
  bossMappingData = await response.json();
}

function getBossName(raidName, bossId, language = 'zh') {
  const raid = bossMappingData[raidName];
  if (!raid) return `Boss #${bossId}`;
  
  const boss = raid.bosses.find(b => b.id === bossId);
  if (!boss) return `Boss #${bossId}`;
  
  return language === 'en' ? boss.name_en : boss.name_zh;
}

// 使用
await loadBossMapping();
console.log(getBossName('NaxxramasWrath', 1)); // 输出: 阿努布雷克汗
console.log(getBossName('NaxxramasWrath', 1, 'en')); // 输出: Anub'Rekhan
```

#### 优化加载 - 按副本加载
```javascript
async function loadBossMappingByRaid(raidName) {
  const response = await fetch(`database/bosses/${raidName}.json`);
  const raidData = await response.json();
  bossMappingData[raidName] = raidData;
}

// 用户选择副本时才加载该副本的BOSS
const raidSelect = document.getElementById('raidSelect');
raidSelect.addEventListener('change', (e) => {
  if (e.target.value) {
    loadBossMappingByRaid(e.target.value);
  }
});
```

### Python

```python
import json

# 加载BOSS数据
with open('database/boss_mapping.json', 'r', encoding='utf-8') as f:
    boss_mapping = json.load(f)

# 获取副本信息
naxx = boss_mapping['NaxxramasWrath']
print(f"副本: {naxx['name_zh']} ({naxx['name_en']})")
print(f"难度: {naxx['difficulty']}")
print(f"BOSS列表:")

for boss in naxx['bosses']:
    print(f"  {boss['id']}. {boss['name_zh']} / {boss['name_en']}")

# 按副本加载优化版
with open('database/bosses/NaxxramasWrath.json', 'r', encoding='utf-8') as f:
    naxx_data = json.load(f)
```

## 在其他网站使用

### WowHead 替代方案

该数据库可作为WowHead的中文本地替代方案：

```javascript
// 假设用户网站
const WoWDatabase = {
  getRaidBosses(raidName, language = 'zh') {
    const raid = bossMappingData[raidName];
    if (!raid) return [];
    return raid.bosses.map(boss => ({
      name: language === 'en' ? boss.name_en : boss.name_zh,
      id: boss.id,
      raid: raidName
    }));
  },
  
  searchBoss(keyword, language = 'zh') {
    const results = [];
    for (const [raidName, raid] of Object.entries(bossMappingData)) {
      raid.bosses.forEach(boss => {
        const name = language === 'en' ? boss.name_en : boss.name_zh;
        if (name.includes(keyword) || name.toLowerCase().includes(keyword.toLowerCase())) {
          results.push({
            name,
            id: boss.id,
            raid: raidName,
            difficulty: raid.difficulty
          });
        }
      });
    }
    return results;
  }
};

// 使用
WoWDatabase.searchBoss('Ragnaros', 'zh');
// [{name: '拉格纳罗斯', id: 9, raid: 'MoltenCore', difficulty: '40-Player Raid'}]
```

## 数据生成脚本

### 创建 (如需添加新副本)
```bash
python create_boss_mapping.py
```

### 验证
```bash
python verify_boss_mapping.py
```

### 分割优化 (从统一文件生成分割文件)
```bash
python split_boss_mapping.py
```

## 未来计划

- [ ] 支持更多扩展包 (Cataclysm, Mists of Pandaria等)
- [ ] 添加BOSS掉落物品关联
- [ ] 支持难度等级差异 (Normal/Heroic/Mythic)
- [ ] 添加首杀时间和进度跟踪
- [ ] GraphQL API 支持
- [ ] RESTful API 服务

## 许可证

本数据库遵循《魔兽世界》粉丝网站政策。
仅供学习和非商业使用。

## 相关资源

- 官方数据来源: WowHead (中英文)
- Altasloot 插件: 游戏内掉落数据库
- 本项目仓库: https://github.com/xungjie/wow_titanreforged_loot
