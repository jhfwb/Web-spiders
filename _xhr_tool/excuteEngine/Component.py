import abc

class Interceptor:
    """拦截器"""
    pass
    # @abc.abstractmethod
    # def handle(self,fuel):
    #     # 导入模块
    #
    #     pass
class ExcuteInterceptor(Interceptor):
    engine=None
    @abc.abstractmethod
    def intercept_before_excute(self, fuel):
        # 导入模块
        pass
    @abc.abstractmethod
    def intercept_after_excute(self, fuel):
        # 导入模块
        pass
class PutExcuteFuelInterceptor(Interceptor):
    """
    在放入执行栈之前的打断器
    """
    @abc.abstractmethod
    def intercept_before_put(self, fuel):
        # 导入模块
        pass
    @abc.abstractmethod
    def intercept_after_excute(self, fuel):
        # 导入模块
        pass
class BackFuelInterceptor(Interceptor):
    """
    在回收Fuel之前和之后的打断器
    """
    @abc.abstractmethod
    def intercept_before_backFuel(self, fuel):
        # 导入模块
        pass
    @abc.abstractmethod
    def intercept_after_backFuel(self, fuel):
        # 导入模块
        pass