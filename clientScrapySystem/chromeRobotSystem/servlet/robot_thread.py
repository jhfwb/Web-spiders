import threading
from queue import Queue

from clientScrapySystem.chromeRobotSystem.utils.RR_Comments import PrintTool
from clientScrapySystem.chromeRobotSystem.innerUtils.web_option_methond import MyOption


class MyPipelineThread(threading.Thread):
    queue=[]
    def __init__(self,driver):
        super().__init__()
        self.readyExcute=Queue()
        self.queue=Queue()
        self.driver=driver
    def put(self,obj):
        self.queue.put(obj)
        return obj
    def run(self):#这个元组放3个位置，执行方法，css选择器，文本内容
        while True:
            acts=self.readyExcute.get()
            messages=[]
            while acts.empty()==False:
                act=acts.get()
                try:
                    PrintTool.print("chromeRobotSystem:"+act['memo'],fontColor="blue")
                    # time.sleep(1)
                except:
                    print("无法找到该memo请确保,memo有被添加。在Action中寻找！！！"+str(act))
                message = MyOption.option(self.driver, options=act)
                if message:
                    if message == "actionFalse":#动作执行失败
                        method=act.get('exception')
                        if method:
                            PrintTool.print("seleniumRobot_exception:该动作失败，正在回调失败方法", fontColor='green')
                            method(act.get('action'))
                        # 动作错误，将动作链条，全部清除
                        if act.get("ignoreErr")==True:
                            break
                    else:#动作执行成功
                        method = act.get('success')
                        if method:
                            PrintTool.print("seleniumRobot_success:该动作成功，正在回调成功方法", fontColor='green')
                            method(act.get('action'))
                        if type(message)!= str:# 当有数据传入的时候
                            messages.append(message)
                        else:# 当没有数据的时候则通过
                            pass
            #一次爬虫完毕：之后保存信息。创建一个专门保存的线程。
            item={}
            for message in messages:
                item.setdefault(message[0],message[1])
            PrintTool.print("成功爬取信息:" +str(item), fontColor='gray')
            self.context.saveThread.queue.put(item)



