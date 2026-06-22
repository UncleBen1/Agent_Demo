from app import history,config
from rich.console import Console
import time
import asyncio
from typing import Callable, Awaitable
import functools
from app.api_client import *
from app.llm_client import *

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
    
    def run() -> None:
        timeit_sync("https://jsonplaceholder.typicode.com/posts/1")
        history.clear_history()  # 删除最后一条历史记录
        Day02().demo_sync()    
        print("\n" + "="*50 + "\n")
        asyncio.run(Day02().demo_post_async())
        print("\n" + "="*50 + "\n")
        asyncio.run(Day02().demo_async())

class Day03 :
    def __init__(self):
        llm_config =config.load_config()
        self.llm_client = LLMClient(
            api_key=llm_config.get("api_key"),
            base_url=llm_config.get("base_url"),
            model=llm_config.get("model_id"),
        )
    
    def demo01(self)->None:

        #回话并且打印
        reply=asyncio.run(self.llm_client.async_chat("你好，我是Jade", "你是一个AI助手"))
        print("AI 回复:", reply)
        history.save_exchange("你好，我是Jade", reply)
        print("====="*30)
        messages = self.llm_client.build_messages_from_history(history.get_history())
        
        messages.append({"role": "user", "content": "我是谁？"})
        reply=asyncio.run(self.llm_client.async_chat(messages))
        print("AI 回复:", reply)
        print("====="*30)
        history.save_exchange("我是谁？", reply)

class Day04:
    def __init__(self):
        llm_config =config.load_config()
        self.llm_client = LLMClient(
            api_key=llm_config.get("api_key"),
            base_url=llm_config.get("base_url"),
            model=llm_config.get("model_id"),
        )
    
    #异步函数计时器装饰器
    def async_timer(func:Callable[...,Awaitable]):
        @functools.wraps(func)
        async def wapper(*args,**kwargs)->Any:
            start = time.perf_counter()
            result = await func(*args,**kwargs)
            elapse = time.perf_counter()-start
            print(f"{func.__name__} 耗时: {elapse:.2f} 秒")
            return result
        return wapper
    
    
    @async_timer
    async def run_serial(self,questions : list[str])->list[tuple[str,str]]:
        result = []
        for q in questions:
            reply = await self.llm_client.async_chat(q, "你是一个AI助手")
            result.append((q, reply))            
        return result
    
    @async_timer
    async def run_concurrent(self,client:LLMClient, questions:list[str])->list[tuple[str,str]]:
        #并发执行
        tasks = [client.async_chat(q, "你是一个AI助手") for q in questions]
        replies = await asyncio.gather(*tasks)
        print(f"问题: {questions}\n回复: {replies}\n{'='*30}")
        return list(zip(questions, replies))
    
    async def run(self)->None:
        
        questions = [
            "什么是人工智能？",
            "Python 的 asyncio 是什么？",
            "如何提高学习效率？",
            "未来十年科技的发展趋势是什么？",
            "你能否推荐一些好书吗？"
        ]
    
        print("=== 串行执行 ===")
        result = await Day04().run_serial(questions)
        print("\n=== 并发执行 ===")
        result =await Day04().run_concurrent(self.llm_client, questions)
        for q, r in result:
            history.save_exchange(q, r)
            print(f"问题: {q}\n回复: {r}\n{'='*30}")
        
        

if __name__ == "__main__":
    #Day03().demo01()
    
    asyncio.run(Day04().run())
