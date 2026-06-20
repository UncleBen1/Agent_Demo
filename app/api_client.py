import httpx
import asyncio

import time
from typing import Any

# 封装同步 Clinet 
#get_json(url,timeout) post_json(url,payload,timeout)

timeout = httpx.Timeout(30.0, connect=5.0)

def get_json(url: str, timeout: httpx.Timeout=timeout) -> dict[str, Any]:
    try:
        with httpx.Client(timeout=timeout) as client:
            resp = client.get(url)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP 状态码错误：{e.response.status_code}")
        return {}
    except httpx.RequestError as e:
        print(f"请求错误：{e}")
        return {}
    except Exception as e:
        print(f"其他错误：{e}")
        return {}

def post_json(url: str, payload: dict, timeout: httpx.Timeout=timeout) -> dict[str, Any]:
    try:
        with httpx.Client(timeout=timeout) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP 状态码错误：{e.response.status_code}")
        return {}
    except httpx.RequestError as e:
        print(f"请求错误：{e}")
        return {}
    except Exception as e:
        print(f"其他错误：{e}")
        return {}

async def async_get_json(url: str, timeout: httpx.Timeout=timeout) -> dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP 状态码错误：{e.response.status_code}")
        return {}
    except httpx.RequestError as e:
        print(f"请求错误：{e}")
        return {}
    except Exception as e:
        print(f"其他错误：{e}")
        return {}

async def async_post_json(url:str, payload: dict, timeout: httpx.Timeout=timeout) -> dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP 状态码错误：{e.response.status_code}")
        return {}
    except httpx.RequestError as e:
        print(f"请求错误：{e}")
        return {}
    except Exception as e:
        print(f"其他错误：{e}")
        return {}

async def async_fetch_multiple(urls: list[str]) -> list[dict[str, Any]]:
    """并发获取多个URL的JSON数据"""
    tasks = [async_get_json(url) for url in urls]
    return await asyncio.gather(*tasks)

def timeit_sync(url:str) -> None:
    start = time.perf_counter()
    try:
        data = get_json(url)
        print(f"同步请求成功，耗时: {time.perf_counter() - start:.2f}秒，数据: {list(data.keys())}")
    except Exception as e:
        print(f"同步请求失败: {e}")
        
        