import requests
import json
import time
import os

# 身份凭证 - 必须与 Fiddler 捕获的一致
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254171e) XWEB/18787",
    "Referer": "https://servicewechat.com/wxe55a89e98174ca75/622/page-frame.html",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}

BASE_URL = "https://wlk.scarlet5.com/trt/mini/db/item/getItemDetail"
OUTPUT_FILE = "wow_db.json"
START_ID = 230101 
END_ID = 250000    

def save_data(data):
    """保存数据到本地 JSON 文件"""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def run_scraper():
    # 初始化或加载现有数据库
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            try:
                database = json.load(f)
            except:
                database = {}
        print(f"已加载现有数据: {len(database)} 条")
    else:
        database = {}

    print(f"执行区间: {START_ID} -> {END_ID}")

    for item_id in range(START_ID, END_ID + 1):
        if str(item_id) in database:
            continue

        try:
            params = {"itemId": item_id}
            response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                # 核心修正：判断 success 标志位，并提取 result 字段
                if result.get("success") == 1 and result.get("result"):
                    item_data = result["result"]
                    database[str(item_id)] = item_data
                    # 打印中文名称
                    print(f"[成功] ID: {item_id} | 名称: {item_data.get('nameCn')}")
                else:
                    # 跳过无物品数据的 ID
                    pass
            elif response.status_code == 403:
                print("错误: 403 Forbidden。凭证过期，请重新获取 Headers。")
                break
            
            # 频率控制：防止触发 WAF 封锁 IP
            time.sleep(0.4)

            # 每获取 20 条记录执行一次磁盘写入
            if item_id % 20 == 0:
                save_data(database)
                print(f"--- 进度保存: {item_id} ---")

        except Exception as e:
            print(f"[异常] ID: {item_id} 错误原因: {e}")
            time.sleep(3)

    save_data(database)
    print("任务完成。")

if __name__ == "__main__":
    run_scraper()