"""
ruoyi_phm 模块初始化入口
======================

框架会以“模块”的形式加载功能。
这个文件的目的就是：
- 把 ruoyi_phm 的路由注册封装在模块内部
- 以后主程序 app.py 不需要为业务模块写任何注册代码

你新增其它模块（ruoyi_alarm / ruoyi_timeseries 等）时，也照这个模式写即可。
"""

def init_app(app):
    # 延迟导入（避免导入时触发复杂依赖/加快启动）
    from ruoyi_phm.controller.prediction import phm_bp

    # 把本模块的蓝图注册到 Flask
    app.register_blueprint(phm_bp)
