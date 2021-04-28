from queue import Queue

from _xhr_tool._annotate import singleObj
from _xhr_tool._utils import relpath
from _xhr_tool._utils.xhr_logger import Logger
from _xhr_tool.chromeRobot.src._chromeRobot_tool.decoratorUtils import DecoratorEngine
from _xhr_tool.chromeRobot.chromeConncet import ChormeDiver
from _xhr_tool.chromeRobot.src.domain.MyInterceptors import ActionIterceptor

from _xhr_tool.excuteEngine.Engine import ExcuteEngine
@singleObj
class ChromeFactory:
    """
    1. 生产动作。
    2. 启动机器引擎，
    3. 启动数据引擎。
    """
    def __init__(self):
        self.logger=Logger(savePath=relpath('../../log/logger.log'))
        from _xhr_tool.chromeRobot.src.domain.MyInterceptors import BackResponse, SaveFindDatas, ExcuteInterval
        driver = ChormeDiver().get_driver()
        self.driver=driver
        # 注册机器人线程
        self.engine=ExcuteEngine()
        self.engine.registerInterceptors(ActionIterceptor,SaveFindDatas,ExcuteInterval,BackResponse)#注册自定义拦截器
        # 注册。。
        self.engine.start()
    def register(self,obj):
        self.user=obj
        setattr(self.user,'store',Queue())
        DecoratorEngine().excuteAllDecorator(obj=self.user,decoratorName='@chrome_robot_excute')

    def getPassageway(self):
        return self._passageway
