import random
from .base import BasePredictor

class MockPredictor(BasePredictor):
    """
    【替身演员】
    这个类假装自己是一个厉害的 AI 模型。
    目前只生成随机数，等你真的 Bi-LSTM 写好了，就把这个文件扔掉。
    """
    
    def predict(self, input_data):
        # 模拟生成 0 到 1 之间的风险概率
        risk_score = random.random() 
        
        # 简单的逻辑：风险越高，健康度越低
        health_index = 100 * (1 - risk_score)
        
        # 简单的逻辑：风险 > 0.8 就报警
        status = "ALARM" if risk_score > 0.8 else "NORMAL"
        
        return {
            "p_cal": round(risk_score, 4),      # 风险概率
            "hi": round(health_index, 2),       # 健康度
            "status": status,                   # 状态
            "source": "Mock Model (Random)"     # 标记：这是假数据
        }