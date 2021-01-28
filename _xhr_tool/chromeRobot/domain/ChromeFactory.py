import inspect
import threading
from queue import Queue

from _xhr_tool._annotate import singleObj
from _xhr_tool._utils import ReflexUtils
from _xhr_tool.chromeRobot._decorator.decoratorUtils import DecoratorEngine
from _xhr_tool.chromeRobot.chromeConncet import ChormeDiver
from _xhr_tool.chromeRobot.servlet.pipeline_thread import MyDataSaveThread
from _xhr_tool.chromeRobot.servlet.robot_thread import MyPipelineThread


@singleObj
class ChromeFactory:
    """
    1. 生产动作。
    2. 启动机器引擎，
    3. 启动数据引擎。
    """
    def __init__(self):
        self._passageway=Queue()
        driver = ChormeDiver().get_driver()
        self.driver=driver
        # 注册机器人线程
        self.robotThread = MyPipelineThread()
        self.robotThread.context = self
        # 注册管道线程
        self.saveThread = MyDataSaveThread()
        self.saveThread.factory = self
        self.robotThread.run()
        self.saveThread.run()

    def register(self,className:type):
        self.user=object.__new__(className)
        setattr(self.user,'store',Queue())
        DecoratorEngine().excuteAllDecorator(obj=self.user,decoratorName='@chrome_robot_excute')
        # self.excuteDecorator(decoratorName='@chrome_robot_excute')


    def getPassageway(self):
        return self._passageway
