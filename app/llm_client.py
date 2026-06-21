import traceback

import httpx
from typing import Any

class LLMClient:
    def __init__(self, api_key: str, base_url: str ,model :str,timeout=60.0):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.timeout = httpx.Timeout(timeout, connect=5.0)
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
                
    #初始化请求头
    def _headers(self) -> dict[str, str]:
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        return self.headers
        
    #封装发送
    async def _response(self, messages: list[dict[str, str]],temperature: float=0.7) -> str:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    
                }
                url = f"{self.base_url.rstrip('/')}/chat/completions"
                resp = await client.post(url, json=payload, headers=self.headers)
                resp.raise_for_status()
                # 模型回复
                return resp.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"HTTP 错误: {e.response.status_code} - {e.response.text}") from e
        except httpx.RequestError as e:
            raise RuntimeError(f"请求错误: {e}") from e
        except Exception as e:
            print("其他错误: ", e)
            traceback.print_exc()
            raise RuntimeError(f"其他错误: {e}") from e

    #单轮回话启用
    async def chat(self,prompt:str,system_prompt:str) -> dict[str,str]:
        messages: list[dict[str,str]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
            ]
        
        # 这里不写入系统提示词
        reply = await self._response(messages)
        return reply
    
    #多轮回话启用
    async def chat_multi(self, messages:list[dict[str,str]]) -> dict[str,str]:
        if not messages:
            raise ValueError("消息列表不能为空")
        reply = await self._response(messages)
        return reply

    def build_messages_from_history(self, history: list[dict[str, str]], system_prompt: str="你是一个AI助手") -> list[dict[str, str]]:
        
        messages = [{"role": "system", "content": system_prompt}]
        for record in history:
            # 从历史记录中提取用户输入和助手输出，构建消息列表
            user_message = record.get("user_input")
            assistant_message = record.get("agent_output")
            if isinstance(user_message, str) and user_message:
                messages.append({"role": "user", "content": user_message})
            if isinstance(assistant_message, str) and assistant_message:
                messages.append({"role": "assistant", "content": assistant_message})
        return messages