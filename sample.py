import requests

# 调用一个公开的 GET 接口（获取随机用户信息）
response = requests.get("https://randomuser.me/api/")
print("状态码:", response.status_code)
print("返回数据:", response.json())   # 解析 JSON