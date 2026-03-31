"""
mock_engine.py - Mock 推理引擎（随机数假数据）
================================================

目的：
- 在真模型没训练好前，先跑通系统链路：前端 → 后端 → 告警/HI → 落库
- 保证接口结构稳定：后面换真模型时，前端不用改、controller不用改

注意：
- 我们尽量让字段“像真模型”：
  raw_score, p_raw, p_cal, ci_low/ci_high, hi, model_version
- 这样等你 Bi-LSTM 跑通，只需要把 factory.py 里选的 engine 换掉即可
"""

import random

from ruoyi_phm.domain.schemas import InferRequest, InferResponse
from .base import InferenceEngine


class MockEngine(InferenceEngine):
    """
    MockEngine：只返回随机数，用于占位。

    seed：
    - 固定 seed 的好处：你每次调用结果“可重复”，便于调试
    - 你想要“每次都不一样”，可以把 seed 改成 None，然后用系统随机
    """

    def __init__(self, seed: int = 42):
        self._rng = random.Random(seed)

    def predict(self, req: InferRequest) -> InferResponse:
        # 1) 生成一个 0~1 的 raw_score（假装是模型输出的异常分数）
        raw_score = self._rng.random()

        # 2) raw 概率：这里先简单用 raw_score 当概率（后期真模型会替换）
        p_raw = min(max(raw_score, 1e-6), 1 - 1e-6)

        # 3) 校准后概率 p_cal（后期你会替换为 Platt / Isotonic）
        #    这里做轻微扰动，模拟“校准”过程
        p_cal = min(max(p_raw * (0.9 + 0.2 * self._rng.random()), 1e-6), 1 - 1e-6)

        # 4) 置信区间（后期你会替换为 MC Dropout / Bootstrap）
        width = 0.05 + 0.15 * self._rng.random()  # 区间宽度 0.05~0.20
        ci_low = max(0.0, p_cal - width)
        ci_high = min(1.0, p_cal + width)

        # 5) HI 健康度（最简公式：HI = 100*(1-p_cal)）
        #    后期你可以把 HI 做成多指标融合/滑动平均/分段映射等
        hi = 100.0 * (1.0 - p_cal)

        # 6) 返回统一结构（非常关键：以后别随便改字段名）
        return InferResponse(
            device_id=req.device_id,
            ts_end=req.ts_end,
            window_minutes=req.window_minutes,
            raw_score=raw_score,
            p_raw=p_raw,
            p_cal=p_cal,
            ci_low=ci_low,
            ci_high=ci_high,
            hi=hi,
            model_version="mock-v0",
            source="mock",
        )
