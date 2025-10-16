import requests
import asyncio
import time
from functools import wraps

def timer_precise(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        elapsed_time = (end- start)
        print(f"⏱️ 函数 {func.__name__} 运行时间: {elapsed_time:.6f} 秒")
        return result
    return wrapper

@timer_precise
async def download_file():
    url = "http://47.76.50.153:8000/"  # 示例网址，返回一个简单的HTML页面
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }  # 模拟浏览器访问，避免被某些网站拒绝[6](@ref)

    try:
        response = requests.get(url, headers=headers, timeout=5)  # 设置超时
        response.raise_for_status()  # 如果状态码不是200，将抛出异常[2](@ref)

        # 将内容保存为HTML文件
        with open('src/webpage.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("网页下载成功！")

    except requests.exceptions.RequestException as e:
        print(f"下载过程中出现错误: {e}")

asyncio.run(download_file())