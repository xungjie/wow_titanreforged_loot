import requests

# 填入你最新的凭证
HEADERS = {
    "User-Agent": "Mozilla/5.0 ...",
    "Referer": "https://servicewechat.com/...",
}

TEST_ID = 235553 # 替换为你确定的 ID

url = f"https://wlk.scarlet5.com/trt/mini/db/item/getItemDetail?itemId={TEST_ID}"
response = requests.get(url, headers=HEADERS)

print(f"状态码: {response.status_code}")
print(f"返回内容: {response.text}")