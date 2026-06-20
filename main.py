from app import config
from app import history

if __name__ == "__main__":
    # 加载配置
    try:
        llm_config = config.load_config()
        print("LLM 配置加载成功：", llm_config)
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
        