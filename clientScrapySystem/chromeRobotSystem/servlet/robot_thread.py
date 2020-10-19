import threading
from queue import Queue


from clientScrapySystem.chromeRobotSystem.innerUtils.web_option_methond import MyOption
from _utils.RR_Comments import PrintTool
class MyPipelineThread(threading.Thread):
    cutMessages=[('',0)]
    queue=[]
    def __init__(self,driver):
        super().__init__()
        self.readyExcute=Queue()
        self.queue=Queue()
        self.driver=driver
        self.itemsQueue=Queue()
    def put(self,obj):
        self.queue.put(obj)
        return obj
    def run(self):#这个元组放3个位置，执行方法，css选择器，文本内容
        reStartSign=False #重启标志
        reStartTime = 0
        while True:
            if reStartSign==False:
                acts=self.readyExcute.get()
            else:
                acts=storeActs
            storeActs = Queue()
            messages=[]
            reStartSign=False
            while acts.empty()==False:
                cutMessage="异常终止ACTION"#1.正常终止。2.异常中止
                act=acts.get()
                storeActs.put(act)
                try:
                    PrintTool.print("chromeRobotSystem:"+act['memo'],fontColor="blue")
                    # time.sleep(1)
                except:
                    print("无法找到该memo请确保,memo有被添加。在Action中寻找！！！"+str(act))
                message = MyOption.option(self.driver, options=act)
                if act.get("monitor")!=None and act.get("monitor")!="":
                    PrintTool.print("seleniumRobot_monitor:正在监听此方法", fontColor='green')
                    act.get("monitor")(self.driver)
                if message:
                    if message == "actionFalse":#动作执行失败
                        method=act.get('exception')
                        if method:
                            PrintTool.print("seleniumRobot_exception:该动作失败，正在回调失败方法", fontColor='green')
                            method(act.get('action'))
                        # 动作错误，将动作链条，全部清除
                        break
                    elif message=='clear_action':
                        cutMessage='正常终止ACTION'
                        break
                    elif message=="reStart_action":
                        reStartTime=reStartTime+1
                        if reStartTime<=2:
                            PrintTool.print("chromeRobotSystem:发生异常:无法找到对应css选择器_执行方案:reStart_action。正在重新调用动作链", fontColor="red")
                            while acts.empty()==False:
                                act = acts.get()
                                storeActs.put(act)
                            reStartSign=True
                            break
                        else:
                            reStartSign = False
                            reStartTime=0
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
            if reStartSign==False:
                item={}
                for message in messages:
                    item.setdefault(message[0],message[1])
                if len(item)==0:
                    PrintTool.print("该信息爬取失败", fontColor='gray')
                    if cutMessage=="正常终止ACTION":
                        self.itemsQueue.put("正常终止ACTION")
                    else:
                        self.itemsQueue.put("异常终止ACTION")
                else:
                    PrintTool.print("成功爬取信息:" +str(item), fontColor='gray', LogPath=PrintTool.LogPath)
                    self.itemsQueue.put(item)




