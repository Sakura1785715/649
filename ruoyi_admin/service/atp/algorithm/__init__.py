"""
算法引擎选择入口（非常重要）
===========================

目的：
- 让 controller / service 永远只依赖“Predictor 接口”，而不是依赖具体模型实现。
- 当前阶段：默认使用 MockPredictor（随机数假数据），用于跑通端到端流程。
- 后期阶段：你只需要把环境变量 PHM_ENGINE 改成 bilstm（或 llm），就能切换到真模型。

为什么不用 USE_MOCK_MODEL = True？
- 写死在代码里会导致：每次切换都要改代码、提交代码、容易出错。
- 环境变量/配置文件才是工程上正确做法：不同环境（开发/测试/线上）用不同配置即可。

用法：
- Windows PowerShell:
    $env:PHM_ENGINE="mock"     # 或 bilstm / llm
    python ruoyi_admin/app.py

- Linux/macOS:
    export PHM_ENGINE=mock
    python ruoyi_admin/app.py
"""

import os

from .base import BasePredictor
from .mock import MockPredictor

# 以后你写好真模型后，再放开这两行（现在先注释掉，避免你还没写就报错）
# from .bilstm import BiLSTMPredictor
# from .llm import LLMPredictor


def get_predictor() -> BasePredictor:
    """
    工厂函数：根据环境变量选择“当前应该用哪个预测器”。

    返回值：
        BasePredictor 的某个实现（Mock / BiLSTM / LLM）

    环境变量：
        PHM_ENGINE:
            - mock   : 使用随机数假数据（默认）
            - bilstm : 使用你训练好的 Bi-LSTM 模型
            - llm    : 使用大模型推理/解释（未来扩展）
    """
    engine = os.getenv("PHM_ENGINE", "mock").strip().lower()

    if engine == "mock":
        # ✅ 当前阶段最推荐：先用假数据把系统链路跑通
        return MockPredictor(seed=42)

    # ====== 下面是后期扩展：你写好对应类后再打开 ======
    # if engine == "bilstm":
    #     return BiLSTMPredictor(model_path=os.getenv("BILSTM_MODEL_PATH", "./models/bilstm.pt"))
    #
    # if engine == "llm":
    #     return LLMPredictor(endpoint=os.getenv("LLM_ENDPOINT"))
    # ====================================================

    # 如果 PHM_ENGINE 写错，直接明确报错，方便你排查
    raise ValueError(f"Unknown PHM_ENGINE={engine}. Allowed: mock / bilstm / llm")

# =========================
# 懒加载单例（非常重要）
# =========================
# 解释：
# - 真模型加载可能很慢/占内存/占显存
# - 如果在 import 时就初始化，会导致启动慢、调试痛苦、多进程重复加载
# - 所以我们第一次真正请求推理时，再创建 predictor，并缓存起来复用
_predictor_instance = None


def get_current_predictor() -> BasePredictor:
    """
    获取“当前正在使用的预测器”单例（懒加载）。

    第一次调用时：根据 PHM_ENGINE 创建 predictor
    后续调用时：直接返回已创建的 predictor，避免重复加载模型
    """
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = get_predictor()
    return _predictor_instance
