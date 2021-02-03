import threading
import time
from queue import Queue
# from clientScrapySystem.chromeRobotSystem.innerUtils.web_option_methond import MyOption
from _xhr_tool._annotate import singleObj, threadingRun
from _xhr_tool._utils.RR_Comments import PrintTool
from _xhr_tool._utils.RUtils import tool
from _xhr_tool.chromeRobot._chromeRobot_tool.actionInterpreter import ActionControlInterpreter
from _xhr_tool.chromeRobot._chromeRobot_tool.excuteLog import ExcuteLog
from _xhr_tool.chromeRobot._chromeRobot_tool.excuteResponsePool import ExcuteResponsePool
from _xhr_tool.chromeRobot._chromeRobot_tool.responseHandle import ResponseHandler
from _xhr_tool.chromeRobot.domain.ChromeFactory import ChromeFactory

from _xhr_tool.chromeRobot.web_option_methond import MyOption

@singleObj
class MyPipelineThread:
    cutMessages=[('',0)]
    queue=[]
    def __init__(self):
        super().__init__()
        self.actQueue=Queue() #执行栈
        self.actionQueue=Queue()
        self.readyAct=Queue()
        self.readyAction=Queue()
        self.excutingQueue=Queue()
    def _pop_excute(self,queue:Queue,func=lambda x:x):
        if queue.qsize()!=0:
            return func(queue.get())
        else:
            return None

    def _getAction(self):
        if self.readyAction.qsize() == 0:
            return self.actionQueue.get()
        else:
            return self.readyAction.get()
    def _getAct(self): # 从准备栈中取出数据，如果准备栈中没有数据，则从执行栈中取出数据
        if self.readyAct.qsize()==0:
            return self.actQueue.get()
        else:
            return self.readyAct.get()
    def excuteActionQueue(self): #将Action队列中的首个Action执行，执行结果是：在acts队列中保存有该Action分解的act
        action=self._getAction()
        while action.acts.qsize()!=0:
            self.actQueue.put(action.acts.get())
        while self.actQueue.qsize()!=0 or self.readyAct.qsize()!=0:
            self.excuteActQueue()
        action._callBackFunc(self)
        ResponseHandler().sendItems()
        # 此处开始
        return action
    def excuteActQueue(self):
        act=self._getAct()
        # 建议此处用日记功能记录一下。
        #控制语句。执行语句。循环语句。
        #判断act的语法。如果是执行
        #创建一个控制中心栈
        select=ActionControlInterpreter().judge(act)
        # print(act)
        if select=="control": #控制语句
            result=ActionControlInterpreter().getControlState()
            # print(result)
            act.get('func')(result)
        elif select=="excute":#执行语句
            # 引入时间器。写入
            ExcuteLog().excutelog(act)
            response = MyOption().option(options=act)
            result=act.get('func')(response) #执行完毕后的回调
            ResponseHandler().handle(response)
            ExcuteResponsePool().backResponse(response)#归还response
            ActionControlInterpreter().putControlState(act=act,result=result)#判断act是否是控制语句，如果是，则将其运行的结果保存在控制栈中。
        #将方法记录起来，留给下一个使用。
        return act


    @threadingRun
    def run(self):
        while True:
            self.excuteActionQueue()




if __name__ == '__main__':
    a=[1,2,3]
    a.append(4)
    a.pop()
    print(a)


