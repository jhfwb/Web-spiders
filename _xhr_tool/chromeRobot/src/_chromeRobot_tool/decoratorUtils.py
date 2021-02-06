from _xhr_tool._annotate import singleObj
from _xhr_tool._utils import ReflexUtils


@singleObj
class DecoratorEngine:
    def __init__(self):
        self._reflexUtils = ReflexUtils()
    def excuteAllDecorator(self,obj,decoratorName="", args=[]):
        """
        执行装饰器下面对应的方法。当只有一个类的,执行之前需要注册
        """
        if obj == None:
            raise ValueError('ChromeFactory没有注册类，无法正常运行该方法。请调用ChromeFactory().register(类名)注册。')
        return self._reflexUtils.excuteAllDecorator(obj=obj, decoratorName=decoratorName, args=args)
    def excuteDecorator(self,obj,decoratorName="", args=[]):
        """
        执行装饰器下面对应的方法。当只有一个类的,执行之前需要注册
        """
        if obj == None:
            raise ValueError('ChromeFactory没有注册类，无法正常运行该方法。请调用ChromeFactory().register(类名)注册。')
        return self._reflexUtils.excuteDecorator(obj=obj, decoratorName=decoratorName, args=args)