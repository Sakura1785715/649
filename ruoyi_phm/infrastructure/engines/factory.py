"""
factory.py - 引擎工厂（配置化 + 懒加载单例）
================================================

为什么需要工厂？
- 让“用哪个模型”变成配置问题，而不是改代码问题
- 你以后可以在不同环境切换：
  PHM_ENGINE=mock / bilstm / llm

为什么需要懒加载单例？
- 真模型（PyTorch）加载很慢、还可能占用显存
- 如果 import 时加载，会导致：
  启动慢、调试痛苦、多进程重复加载
- 所以：第一次调用 get_engine() 时再加载，并缓存复用

✅ 你未来接入真模型时，只需要：
1) 新写一个 bilstm_engine.py，实现 InferenceEngine
2) 在 create_engine() 里加一个 elif 分支
3) export PHM_ENGINE=bilstm
其余代码不动
"""

import os
from typing import Optional

from .base import InferenceEngine
from .mock_engine import MockEngine

# 模块级缓存：保存单例
_engine_instance: Optional[InferenceEngine] = None


def create_engine() -> InferenceEngine:
    """
    只负责“创建”一个引擎实例，不缓存。
    缓存逻辑在 get_engine()。
    """
    engine = os.getenv("PHM_ENGINE", "mock").strip().lower()

    if engine == "mock":
        return MockEngine(seed=42)

    # ====== 后期扩展：写好再打开 ======
    # if engine == "bilstm":
    #     from .bilstm_engine import BiLSTMEngine
    #     model_path = os.getenv("BILSTM_MODEL_PATH", "./models/bilstm.pt")
    #     return BiLSTMEngine(model_path=model_path)
    #
    # if engine == "llm":
    #     from .llm_engine import LLMEngine
    #     endpoint = os.getenv("LLM_ENDPOINT", "")
    #     return LLMEngine(endpoint=endpoint)
    # =================================

    raise ValueError(f"Unknown PHM_ENGINE={engine}. Allowed: mock / bilstm / llm")


def get_engine() -> InferenceEngine:
    """
    获取引擎单例（懒加载）。
    你在任何地方需要推理，只调用这个函数。
    """
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = create_engine()
    return _engine_instance
