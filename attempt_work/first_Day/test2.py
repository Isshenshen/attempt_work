import asyncio
import aiohttp
import time
import aiofiles


async def download_single(session, url, save_path, index):
    """下载单个文件 - 添加详细日志"""
    print(f"🚀 任务{index} 开始: {url}")
    start_time = time.time()

    try:
        async with session.get(url) as response:
            request_time = time.time() - start_time
            print(f"📥 任务{index} 收到响应: {response.status} (请求耗时: {request_time:.2f}s)")

            if response.status == 200:
                await asyncio.sleep(1)
                content = await response.read()
                read_time = time.time() - start_time - request_time
                print(f"📖 任务{index} 读取内容完成 (读取耗时: {read_time:.2f}s)")
                await asyncio.sleep(1)
                async with aiofiles.open(save_path, 'wb') as f:
                    await f.write(content)

                total_time = time.time() - start_time
                print(f"✅ 任务{index} 完成: 总耗时 {total_time:.2f}s")
                return True, f"下载成功: {url}"
            else:
                total_time = time.time() - start_time
                print(f"❌ 任务{index} HTTP错误: {response.status} (总耗时: {total_time:.2f}s)")
                return False, f"HTTP错误: {response.status}"
    except Exception as e:
        total_time = time.time() - start_time
        print(f"💥 任务{index} 异常: {e} (总耗时: {total_time:.2f}s)")
        return False, f"错误: {str(e)}"


async def download_multiple_async(urls, save_dir):
    """异步并发下载多个文件"""
    print(f"🔄 开始并发下载 {len(urls)} 个URL")
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [download_single(session, url, f"{save_dir}/webpage_{i}.html", i)
                 for i, url in enumerate(urls)]
        results = await asyncio.gather(*tasks)

        total_time = time.time() - start_time
        print(f"🎯 所有任务完成，总耗时: {total_time:.2f}s")
        return results


def main():
    """主函数"""
    test_urls = [
        "http://httpbin.org/ip",  # 快速响应
        "http://httpbin.org/user-agent",  # 快速响应
        "http://httpbin.org/delay/2",  # 2秒延迟
    ]
    url = "http://47.76.50.153:8000/"
    test_urls = [url] * 100
    print("=== 异步并发下载测试 ===")
    print(f"测试URLs: {test_urls}")
    print()

    start_time = time.time()
    results = asyncio.run(download_multiple_async(test_urls, "downloaded_pages"))
    elapsed_time = time.time() - start_time

    print(f"\n⏱️ 总运行时间: {elapsed_time:.6f} 秒")

    # 分析结果
    if elapsed_time < 4:  # 如果总时间小于4秒，说明并发有效
        print("✅ 异步并发工作正常！")
    else:
        print("❌ 异步并发可能未正常工作")

    for success, message in results:
        status = "✅" if success else "❌"
        print(f"{status} {message}")


if __name__ == "__main__":
    main()