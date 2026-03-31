"""
schemas.py - 领域层请求/响应结构（非常重要）
========================================

这里定义“推理接口”的输入/输出数据结构（契约）。

为什么一定要有 schemas？
- 让 controller / service / engine 的数据结构统一，避免到处散落 dict
- 让你后期换模型（Mock -> BiLSTM -> LLM）时，外部不需要改
- 未来你要落库、做告警映射、画前端图表，也都依赖这些字段

字段说明（与你的 PRD 思路一致）：
- raw_score: 模型原始异常分数（任意范围都行，但建议 0~1）
- p_raw    : 原始概率（未校准）
- p_cal    : 校准后概率（后期可做 Platt/Isotonic）
- ci_low/ci_high: 置信区间（后期可做 MC Dropout/Bootstrap）
- hi       : 健康度 Health Index（0~100）
- model_version/source: 便于追踪你现在用的是什么模型/引擎（很重要）
"""

from pydantic import BaseModel, Field


class InferRequest(BaseModel):
    """
    推理请求

    说明：
    - 前期你可以只传 device_id/ts_end/window_minutes
    - 后期接入 InfluxDB 后，你可以再扩展：features、metrics 等字段
    """
    device_id: str = Field(..., description="设备唯一标识，例如设备编号/台账ID")
    ts_end: str = Field(..., description="窗口结束时间（ISO8601 字符串）")
    window_minutes: int = Field(60, ge=1, description="回看窗口长度（分钟）")


class InferResponse(BaseModel):
    """
    推理响应（你尽量不要改这些字段名，否则前端/告警会跟着改）
    """
    device_id: str
    ts_end: str
    window_minutes: int

    raw_score: float
    p_raw: float
    p_cal: float
    ci_low: float
    ci_high: float
    hi: float

    model_version: str
    source: str
