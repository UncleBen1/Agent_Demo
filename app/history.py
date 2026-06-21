import json
from datetime import datetime
from pathlib import Path


HISTORY_FILE = Path(__file__).resolve().parent.parent / 'history.jsonl'


def save_exchange(user_input: str, agent_output: str) -> None:
    """流式追加保存一次对话：用户输入 + Agent 输出，并记录时间戳。

    以 JSONL（每行一个 JSON 对象）形式追加写入，无需读取已有内容，
    适合记录量大、写入频繁的场景。

    Args:
        user_input: 用户对 Agent 的输入。
        agent_output: Agent 的输出。
    """
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "user_input": user_input,
        "agent_output": agent_output,
    }
    # 采用追加模式
    with HISTORY_FILE.open('a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')


def get_history() -> list[dict]:
    """按行读取全部历史记录，跳过空行与损坏的行。"""
    if not HISTORY_FILE.exists():
        return []
    history: list[dict] = []
    with HISTORY_FILE.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                history.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return history

def limit_history(max_records: int = 100) -> list[dict]:
    """获取最近的 N 条历史记录，默认 100 条。"""
    history = get_history()
    return history[-max_records:]


def clear_history() -> None:
    """清空历史记录。"""
    HISTORY_FILE.write_text('', encoding='utf-8')


