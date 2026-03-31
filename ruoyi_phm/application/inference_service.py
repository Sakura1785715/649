"""
inference_service.py - 推理用例服务（Application Layer）
=======================================================

这一层的意义（非常重要）：
- controller（HTTP）只负责：拿到请求 JSON -> 调用 service -> 返回 JSON
- engine（模型）只负责：predict(req) -> resp
- service 负责“编排流程”（业务流程的中枢）：

    未来你会在这里逐步加入：
    1) 从 InfluxDB 拉取时序窗口数据
    2) 特征提取（滑动窗口、归一化、对齐）
    3) 调用模型推理（Bi-LSTM/LLM）
    4) 概率校准 + 置信区间计算
    5) HI 计算 + 告警映射（生成告警/去抖/分级）
    6) 结果落库（MySQL）

✅ 现在阶段（MVP）：
- 不接 InfluxDB
- 直接调用 MockEngine 返回假数据
"""

from ruoyi_phm.domain.schemas import InferRequest, InferResponse
from ruoyi_phm.infrastructure.engines.factory import get_engine


class InferenceService:
    """
    推理服务：对外提供 infer() 方法。
    controller 只与这个类交互。
    """

    def infer(self, req: InferRequest) -> InferResponse:
        """
        当前最简单版本：直接调用引擎预测。

        后续扩展建议（写在这里，不要写到 controller）：
        - 如果你要接 InfluxDB：
            series = influx_client.query_window(req.device_id, req.ts_end, req.window_minutes)
            features = feature_extractor.transform(series)
            req.features = features   #（需要你在 InferRequest 里扩展字段）
        - 然后再 engine.predict(req)
        """
        engine = get_engine()
        return engine.predict(req)
