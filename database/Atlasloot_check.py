import os
import re
import requests
import json
import time

# --- 配置区 ---
# AtlasLoot 路径
ATLAS_PATH = r"C:\Users\Jie\Desktop\wow_Loot\Altasloot"
# 身份凭证（沿用你之前的成功凭据）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254171e) XWEB/18787",
    "Referer": "https://servicewechat.com/wxe55a89e98174ca75/622/page-frame.html"
}
BASE_URL = "https://wlk.scarlet5.com/trt/mini/db/item/getItemDetail"
OUTPUT_FILE = "atlas_items_db.json"

def extract_ids_from_atlas():
    """从本地 AtlasLoot 文件中提取所有物品 ID"""
    print(f"正在分析目录: {ATLAS_PATH}")
    item_ids = set()
    # 匹配 5 到 6 位的数字（魔兽常见物品 ID 区间）
    id_pattern = re.compile(r'\b(\d{5,6})\b')

    for root, dirs, files in os.walk(ATLAS_PATH):
        for file in files:
            if file.endswith(('.lua', '.txt')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        matches = id_pattern.findall(content)
                        for m in matches:
                            # 过滤掉不合理的 ID (例如时光服通常在 200000 以上)
                            # 如果需要抓取低级装备，可以调整此阈值
                            if int(m) > 1000: 
                                item_ids.add(int(m))
                except Exception as e:
                    print(f"无法读取文件 {file}: {e}")
    
    print(f"分析完成。共提取到 {len(item_ids)} 个唯一物品 ID。")
    return sorted(list(item_ids))

def run_scraper(target_ids):
    """根据提取的 ID 列表定向爬取数据"""
    database = {}
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            try:
                database = json.load(f)
            except:
                database = {}
        print(f"已加载现有数据: {len(database)} 条")

    print(f"开始定向抓取...")

    for count, item_id in enumerate(target_ids, 1):
        if str(item_id) in database:
            continue

        try:
            params = {"itemId": item_id}
            response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") == 1 and result.get("result"):
                    item_data = result["result"]
                    database[str(item_id)] = item_data
                    print(f"[{count}/{len(target_ids)}] 成功: {item_id} | {item_data.get('nameCn')}")
                else:
                    # 对于 AtlasLoot 存在但数据库没有的 ID，标记为空以防重复尝试
                    database[str(item_id)] = None 
            
            # 频率控制
            time.sleep(0.3)

            # 每 50 条保存一次
            if count % 50 == 0:
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    json.dump(database, f, ensure_ascii=False, indent=4)
                print(f"--- 进度已保存 ---")

        except Exception as e:
            print(f"ID {item_id} 请求异常: {e}")
            time.sleep(2)

    # 最终保存
    # 过滤掉为 None 的记录，保持 JSON 纯净
    final_db = {k: v for k, v in database.items() if v is not None}
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_db, f, ensure_ascii=False, indent=4)
    print(f"全部任务完成。最终有效物品总数: {len(final_db)}")

if __name__ == "__main__":
    # 1. 提取 ID
    ids = extract_ids_from_atlas()
    if ids:
        # 2. 开始抓取
        run_scraper(ids)
    else:
        print("未在指定目录找到任何有效物品 ID，请检查路径。")