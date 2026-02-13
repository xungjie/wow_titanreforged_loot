import os
import re
import requests
import json
import time

# --- 配置区 ---
ATLAS_PATH = r"C:\Users\Jie\Desktop\wow_Loot\Altasloot"
# 身份凭证
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254171e) XWEB/18787",
    "Referer": "https://servicewechat.com/wxe55a89e98174ca75/622/page-frame.html"
}
BASE_URL = "https://wlk.scarlet5.com/trt/mini/db/item/getItemDetail"
OUTPUT_FILE = "tempest_keep_db.json"

# 风暴要塞相关的关键词（AtlasLoot 内部通常使用英文 ID 或特定标签）
TK_KEYWORDS = ["TempestKeep", "TheEye", "风暴要塞", "Kael'thas"]

def get_tk_item_ids():
    """从 AtlasLoot 中精准提取风暴要塞的物品 ID"""
    print(f"正在扫描风暴要塞相关数据...")
    tk_ids = set()
    # 匹配 5 位数字的正则（T5 级别装备通常是 5 位，如 29988）
    id_pattern = re.compile(r'\b(\d{5})\b')

    for root, dirs, files in os.walk(ATLAS_PATH):
        for file in files:
            if file.endswith('.lua'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # 检查文件是否包含风暴要塞关键词
                        if any(kw in content for kw in TK_KEYWORDS):
                            matches = id_pattern.findall(content)
                            for m in matches:
                                # 过滤掉非物品 ID（如版本号 30300 等）
                                if 29000 <= int(m) <= 35000 or int(m) > 200000:
                                    tk_ids.add(int(m))
                except Exception as e:
                    pass
    
    print(f"提取完成。在风暴要塞配置中找到 {len(tk_ids)} 个潜在物品 ID。")
    return sorted(list(tk_ids))

def run_scraper(item_list):
    """定向抓取数据"""
    database = {}
    print(f"开始抓取风暴要塞物品详情...")

    for count, item_id in enumerate(item_list, 1):
        try:
            params = {"itemId": item_id}
            response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") == 1 and result.get("result"):
                    item_data = result["result"]
                    # 验证是否为有效物品（有时 AtlasLoot 里的数字是坐标）
                    if item_data.get('nameCn'):
                        database[str(item_id)] = item_data
                        print(f"[{count}/{len(item_list)}] 成功: {item_data.get('nameCn')}")
            
            # 频率控制，MVP 规模小，可以稍微快一点点
            time.sleep(0.2)

        except Exception as e:
            print(f"ID {item_id} 错误: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(database, f, ensure_ascii=False, indent=4)
    
    print(f"\nMVP 数据库已生成！")
    print(f"文件位置: {os.path.abspath(OUTPUT_FILE)}")
    print(f"共计有效物品: {len(database)} 个")

if __name__ == "__main__":
    # 1. 提取 ID
    target_ids = get_tk_item_ids()
    if target_ids:
        # 2. 抓取
        run_scraper(target_ids)
    else:
        print("错误：未能在 AtlasLoot 目录中定位到风暴要塞数据，请确认路径或关键词。")