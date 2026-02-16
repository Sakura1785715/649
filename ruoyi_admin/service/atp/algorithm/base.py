from abc import ABC, abstractmethod

class BasePredictor(ABC):
    """
    【核心契约】
    这是所有预测模型的“老祖宗”。
    它规定了：只要想在这个系统里当模型，就必须有一个叫 predict 的功能。
    这样设计后，系统只认这个标准，不认具体是谁，实现了“低耦合”。
    """
    
    @abstractmethod
    def predict(self, input_data):
        """
        标准预测接口
        :param input_data: 输入的数据
        :return: 必须返回一个字典，包含 p_cal(风险概率) 和 hi(健康度)
        """
        pass