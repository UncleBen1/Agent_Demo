import traceback

import httpx
from typing import Any

class LLMClient:
    def __init__(self, api_key: str, base_url: str ,model :str,timeout=60.0):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.timeout = httpx.Timeout(timeout, connect=5.0)
        
                
    #初始化请求头
    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
    #组装链接
    def _link_url(self) ->str:
        return f"{self.base_url.rstrip('/')}/chat/completions"
    #状态检查
    def _status_check(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise RuntimeError("❌ 401：鉴权失败，检查 API Key 是否正确/是否过期")
        elif response.status_code == 403:
            raise RuntimeError(f"服务器拒接执行")
        elif response.status_code == 405:
            raise RuntimeError(f"请求方法不被允许")
        elif response.status_code == 429:
            raise RuntimeError(f"请求过于频繁，请稍后再试")
        elif response.status_code >= 500:
            raise RuntimeError(f"服务器错误: {response.status_code} - {response.text}")
        response.raise_for_status()    
    #提取回复内容    
    def _exact_content(self, response:dict[str,Any]) -> str:
        """从响应中提取模型回复内容"""
        try:
            return response.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as e:
            print("解析响应时出错：", e)
            traceback.print_exc()
            return "解析响应时出错，请检查日志。"
    
    #封装发送
    async def _request_async(self, messages: list[dict[str, str]],temperature: float=0.7) -> str:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                payload={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    
                }
                resp = await client.post(self._link_url(), json=payload, headers=self._headers())
                self._status_check(resp)
                # 模型回复
                return self._exact_content(resp.json())
        except Exception as e:
            print("请求模型时出错：", e)
            traceback.print_exc()
            return "请求模型时出错，请检查日志。"
        
    #会话启用
    async def async_chat(self,prompt:str,system_prompt:str) -> dict[str,str]:
        messages: list[dict[str,str]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
            ]
        
        reply = await self._request_async(messages)
        return reply
    
    async def async_chat_with_history(self, history: list[dict[str, str]], new_prompt: str, system_prompt: str="你是一个AI助手") -> str:
        messages = self.build_messages_from_history(history, system_prompt)
        messages.append({"role": "user", "content": new_prompt})
        reply = await self._request_async(messages)
        return reply

    def build_messages_from_history(self, history: list[dict[str, str]], system_prompt: str="你是一个AI助手") -> list[dict[str, str]]:
        
        messages = [{"role": "system", "content": system_prompt}]
        for record in history:
            # 从历史记录中提取用户输入和助手输出，构建消息列表
            user_message = record.get("user_input")
            assistant_message = record.get("agent_output")
            if isinstance(user_message, str) and user_message:
                messages.append({"role": "user", "content": user_message})
                #如果历史记录中的用户输入不为空，则添加到消息列表中
            if isinstance(assistant_message, str) and assistant_message:
                messages.append({"role": "assistant", "content": assistant_message})
        return messages
