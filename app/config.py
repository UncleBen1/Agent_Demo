import os
from pathlib import Path
from dotenv import load_dotenv


def load_config() -> dict[str, str]:
    """加载目录 .env文件 返回LLM相关配置 """
    env_path = Path(__file__).resolve().parent.parent / '.env'
    
    if not env_path.exists():
        raise FileNotFoundError(f"配置文件 .env 不存在于路径: {env_path}")
    load_dotenv(dotenv_path=env_path)
    api_key = os.getenv('LLM_API_KEY')
    if not api_key:
        raise ValueError("LLM_API_KEY 未在 .env 文件中设置")
    return {
        "api_key": api_key,
        "base_url": os.getenv('LLM_BASE_URL') or "None | Check .env",
        "model_id": os.getenv('LLM_MODEL_ID') or "None | Check .env",
    }
