from _xhr_tool.excuteEngine.Component import ExcuteInterceptor
import logging
class LogInterceptor(ExcuteInterceptor):# 保存find方法的。
    """
    保存输出的数据。当出现异常的时候，则
    """
    def __init__(self):
        pass
    def intercept_before_excute(self,fuel):
        if fuel.get_func()!=None:
            logging.warning(fuel.get_func().__name__+"  "+str(fuel.get_func_kwargs()))
    def intercept_after_excute(self,fuel):
        pass