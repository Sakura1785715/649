"""
prediction.py - 推理接口 Controller（薄层）
========================================

要求：
- controller 必须保持“薄”，不要写业务逻辑
- 只做三件事：
  1) 解析请求 JSON
  2) 调用 InferenceService
  3) 返回 JSON 响应

路径保持不变：
- 你以前的路径是：/atp/prediction/infer
- 为了让前端/联调不改，我们这里也保持这个路径
"""

from flask import Blueprint, request, jsonify

from ruoyi_phm.application.inference_service import InferenceService
from ruoyi_phm.domain.schemas import InferRequest

# ✅ url_prefix 保持与你原来一致：/atp/prediction
phm_bp = Blueprint("phm_bp", __name__, url_prefix="/atp/prediction")

_service = InferenceService()


@phm_bp.route("/infer", methods=["POST"])
def infer():
    """
    推理接口

    请求 JSON 示例：
    {
      "device_id": "demo-001",
      "ts_end": "2026-02-16T00:00:00",
      "window_minutes": 60
    }

    响应 JSON 示例（MockEngine）：
    {
      "device_id": "...",
      "raw_score": 0.12,
      "p_raw": 0.12,
      "p_cal": 0.11,
      "ci_low": 0.02,
      "ci_high": 0.25,
      "hi": 89.0,
      "model_version": "mock-v0",
      "source": "mock",
      ...
    }
    """
    payload = request.get_json(force=True) or {}

    # 1) 用 Pydantic 做参数校验（字段缺失会直接报错，便于你排查）
    req = InferRequest(**payload)

    # 2) 调用业务服务
    resp = _service.infer(req)

    # 3) 返回 JSON
    #    Pydantic v2: model_dump()
    #    Pydantic v1: dict()
    return jsonify(resp.model_dump())
