from flask import Blueprint, jsonify
# 注意：这里我们引用的是第四步的“全局变量”，而不是具体的 Mock 类
# 这就是“依赖倒置原则”，代码耦合度极低！
from ruoyi_admin.service.atp.algorithm import get_current_predictor

atp_bp = Blueprint('atp_prediction', __name__, url_prefix='/atp/prediction')

@atp_bp.route('/infer', methods=['GET', 'POST'])
def infer():
    try:
        # 1. 未来这里会接收前端传来的设备ID
        # input_data = request.json 
        
        # 2. 调用核心算法（不管它是谁，反正它能 predict）
        predictor = get_current_predictor()
        result = predictor.predict([])
        
        # 3. 返回标准格式
        return jsonify({
            "code": 200,
            "msg": "操作成功",
            "data": result
        })
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)})