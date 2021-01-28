import time
from queue import Queue
from _xhr_tool._annotate import threadingRun
from _xhr_tool.chromeRobot._decorator.decoratorUtils import DecoratorEngine


class MyDataSaveThread:

    @threadingRun
    def run(self):
        from _xhr_tool.chromeRobot.domain.ChromeFactory import ChromeFactory
        chromeFactory=ChromeFactory()
        while True:
            items=chromeFactory.getPassageway().get()
            DecoratorEngine().excuteDecorator(obj=chromeFactory.user,decoratorName='@chrome_datas_catch',args=[items])

