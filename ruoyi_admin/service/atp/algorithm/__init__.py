from .mock import MockPredictor
# from .lstm import LstmPredictor  <-- 未来你的真模型放在这里引入

# ==========================================
#  【核心开关】
#  True  = 使用随机数假模型（当前阶段）
#  False = 使用真实 AI 模型（未来阶段）
# ==========================================
USE_MOCK_MODEL = True 

def get_predictor():
    if USE_MOCK_MODEL:
        print("【系统提示】当前正在使用 MOCK (随机数) 模型")
        return MockPredictor()
    else:
        # return LstmPredictor() <-- 未来这里返回真模型
        pass

# 创建一个全局唯一的模型实例
# 所有的业务代码都只调用这个 current_predictor，根本不知道底下是真是假
current_predictor = get_predictor()