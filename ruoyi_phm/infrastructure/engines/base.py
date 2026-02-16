"""
base.py - 推理引擎接口（最关键的“可替换点”）
================================================

你以后无论用：
- Mock（随机数假数据）
- 真模型（Bi-LSTM / Transformer）
- 大模型（LLM 远程推理/解释）

都必须实现同一个接口：predict(req) -> resp

这样你项目其它地方（controller/application）永远不用改。
你只需要在 factory.py 里切换用哪个引擎即可。

✅ 这就是“高内聚、低耦合、可维护、可扩展”的核心做法：
- 业务流程依赖“接口”(抽象)
- 具体实现放在 infrastructure/engines 里（随时替换）
"""

from abc import ABC, abstractmethod

from ruoyi_phm.domain.schemas import InferRequest, InferResponse


class InferenceEngine(ABC):
    """
    推理引擎接口（契约）

    约束：
    - 所有引擎必须实现 predict()
    - predict() 输入/输出必须严格遵守 schemas.py 定义
      （这样前端、告警规则、数据库都能稳定）
    """

    @abstractmethod
    def predict(self, req: InferRequest) -> InferResponse:
        """
        根据输入请求 req，返回统一结构 InferResponse

        注意：
        - 这里不做 Flask request 解析，也不做 HTTP 返回
        - 这里只做“纯推理逻辑”，保持干净、可测试
        """
        raise NotImplementedError
