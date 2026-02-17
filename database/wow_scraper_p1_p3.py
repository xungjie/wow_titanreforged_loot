import os
import re
import requests
import json
import time

# --- 配置区 ---
ATLAS_PATH = r"C:\Users\Jie\Desktop\wow_Loot\Altasloot"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254171e) XWEB/18787",
    "Referer": "https://servicewechat.com/wxe55a89e98174ca75/622/page-frame.html"
}
BASE_URL = "https://wlk.scarlet5.com/trt/mini/db/item/getItemDetail"
OUTPUT_FILE = "wlk_raids_db.json"

# 副本关键字（用于从文件中筛选 ID）
RAID_KEYWORDS = ["Naxxramas", "Kel'Thuzad", "纳克萨玛斯", "EyeOfEternity", "Malygos", "永恒之眼", "ObsidianSanctum", "Sartharion", "黑曜石圣殿", "MoltenCore", "Ragnaros", "熔火之心"]

def get_item_ids_relaxed():
    print(f"正在扫描目录: {ATLAS_PATH} ...")
    found_ids = set()
    # 匹配 5-6 位数字
    id_pattern = re.compile(r'\b(\d{5,6})\b')
    
    for root, dirs, files in os.walk(ATLAS_PATH):
        # 只跳过明显的 Classic 基础包，防止数据量过大
        if "AtlasLoot_Classic" in root and "Wrath" not in root:
            continue

        for file in files:
            if file.endswith('.lua'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # 只要文件里包含副本关键字，就提取其中的所有 ID
                        if any(kw in content for kw in RAID_KEYWORDS):
                            matches = id_pattern.findall(content)
                            for m in matches:
                                item_id = int(m)
                                # 只要是 5 位以上的 ID 都先列入考察名单
                                if item_id > 10000:
                                    found_ids.add(item_id)
                except:
                    pass
    
    print(f"分析完成。找到 {len(found_ids)} 个潜在物品 ID，准备开始 API 筛选...")
    return sorted(list(found_ids))

def run_scraper(item_list):
    database = {}
    # 支持断点续传
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            try: database = json.load(f)
            except: database = {}

    total = len(item_list)
    for i, item_id in enumerate(item_list, 1):
        if str(item_id) in database: continue

        try:
            params = {"itemId": item_id}
            response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") == 1 and result.get("result"):
                    item_data = result["result"]
                    
                    # 【核心筛选】只保留 80 级装备，或者时光服自定义装备（200000+）
                    # 时光服重铸的 MC 装备通常也是 80 级
                    is_wlk_item = item_data.get('requiredLevel') == 80
                    is_custom_item = item_id > 200000 
                    
                    if is_wlk_item or is_custom_item:
                        database[str(item_id)] = item_data
                        print(f"[{i}/{total}] 采集到 WLK 装备: {item_data.get('nameCn')} (ID: {item_id})")
                    else:
                        # 标记为 None 避免重复爬取这些 60 级的杂质
                        database[str(item_id)] = None 
            
            # 频率控制
            time.sleep(0.3)
            if i % 50 == 0:
                # 存盘时过滤掉 None
                clean_db = {k: v for k, v in database.items() if v is not None}
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    json.dump(clean_db, f, ensure_ascii=False, indent=4)
                print(f"--- 进度已保存，当前有效 WLK 物品: {len(clean_db)} ---")

        except Exception as e:
            time.sleep(1)

    # 最终保存
    clean_db = {k: v for k, v in database.items() if v is not None}
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(clean_db, f, ensure_ascii=False, indent=4)
    print(f"抓取结束。有效 80 级/重铸装备总数: {len(clean_db)}")

if __name__ == "__main__":
    target_ids = get_item_ids_relaxed()
    if target_ids:
        run_scraper(target_ids)
    else:
        print("未发现任何 ID，请确认 C:\\Users\\Jie\\Desktop\\wow_Loot\\Altasloot 路径是否正确。")