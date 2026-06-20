from app import config
from app import history
from rich.console import Console
import time
import asyncio
from app.api_client import *

console = Console()
#text
payload = {"User": "HuangJUe", "Message": "Hello, World!"}

def day01()->None:
    # 加载配置
    try:
        llm_config = config.load_config()
    except (FileNotFoundError, ValueError) as e:
        print("加载配置时出错：", e)
        exit(1)

    user_input = input("User Input: ")
    # 记录历史
    try:
        history.save_exchange(user_input, "这是一个模拟的 Agent 输出。")
        print("历史记录已保存到文件。")
    except Exception as e:
        print("保存历史记录时出错：", e)
        exit(1)

class Day02:
    def demo_sync(self) -> None:
        """演示同步请求"""
        url = "https://jsonplaceholder.typicode.com/posts/1"
        data = get_json(url)
        history.save_exchange("同步请求示例", str(data))
        console.print(data,style="green")
        
    async def demo_async(self) -> None:
        """演示异步请求"""
        start = time.perf_counter()
        urls = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 6)]
        result = await async_fetch_multiple(urls)
        for i, data in enumerate(result, 1):
            history.save_exchange(f"异步请求示例 {i}", str(data))
            console.print(data, style="cyan")
        end = time.perf_counter()
        print(f"异步请求耗时: {end - start:.2f} 秒")

    async def demo_post_async(self) ->None : 
        start = time.perf_counter()
        url = "https://jsonplaceholder.typicode.com/posts"
        result =await async_post_json(url, payload)
        history.save_exchange("异步POST请求示例", str(result))
        console.print(result, style="magenta")
        end = time.perf_counter()
        print(f"异步POST请求耗时: {end - start:.2f} 秒")


if __name__ == "__main__":
    
    ##Day02 text
    timeit_sync("https://jsonplaceholder.typicode.com/posts/1")
    history.clear_history()  # 删除最后一条历史记录
    Day02().demo_sync()    
    print("\n" + "="*50 + "\n")
    asyncio.run(Day02().demo_post_async())
    print("\n" + "="*50 + "\n")
    asyncio.run(Day02().demo_async())