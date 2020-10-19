import threading
from queue import Queue
from types import MethodType,FunctionType
import time
from _utils.RR_Comments import ReflexTool, JudgeType, PrintTool


class Engine:
    """
    引擎：能够更好地异步执行代码。
    1.启动引擎 start
    2.关闭引擎 close
    3.运行特定方法 put
    4.运行一次引擎 work
    5.
    """
    def __init__(self):
        self.executeTasks={}
        self.log=[]
        self.q=Queue()
        self.status=0
        self.ready=[]
        self.sign = 1
        # self.thread=threading.Thread(target=producter,args=["子线程1"])
        self.thread=""
    def setExecuteTask(self,name="",task={}):
        self.executeTasks.setdefault(name,task)
    def getExecuteTask(self,name=""):
        return self.executeTasks.get(name)
    def start(self):#启动引擎
        PrintTool.print('引擎启动中...',fontColor='gray')
        self.thread=threading.Thread(target=self._run,args=[]).start()
        return self
    def _run(self):
        while self.sign==1:
            functionAndOption=self.q.get()
            function=functionAndOption[0]
            option=functionAndOption[1]
            message=ReflexTool.execute(function,option)
            self.log.append("时间:"+str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+"_运行函数"+str(function))
    def execute(self,taskNames=[]):
        """
        无视一切。直接执行方法。
        执行方法。
        immediately:
        立即执行
        Timing
        定时执行
        """
        if type(taskNames)==type(""):
            taskNames=[taskNames]
        if type(taskNames)==type([]):
            for taskName in taskNames:
                task=self.getExecuteTask(taskName)
                if task==None:
                    raise ValueError("找不到该任务")
                if task.store['mode']=="immediately":
                    for functionsAndOption in task.functionsAndOptions:
                        self._executeImmediately(functionsAndOption[0],functionsAndOption[1])
                elif task.store['mode']=="Timing":
                    task.store['isExecute'] = True
                    self._executeTiming(task,executeNum=task.store['executeNum'])
        else:
            raise ValueError('类型错误'+taskNames)
    def _executeTiming(self,task,starSign=0,executeNum=0):
        if executeNum<0:
            if starSign==1:
                for functionsAndOption in task.store['functionsAndOptions']:
                    self._executeImmediately(functionsAndOption[0],functionsAndOption[1])
            starSign=1
            if task.store['clear'] == True:
                task.store['clear']=False
                task.store['isExecute'] = False
                return
            threading.Timer(task.store['interval'], self._executeTiming,args=[task,starSign,executeNum]).start()
        else:
            if executeNum==0 or task.store['clear']==True:
                task.store['clear'] = False
                task.store['isExecute'] = False
                return
            if starSign==1:
                for functionsAndOption in task.store['functionsAndOptions']:
                    self._executeImmediately(functionsAndOption[0], functionsAndOption[1])
            if starSign==0:
                executeNum = executeNum + 1
            starSign=1
            executeNum = executeNum - 1
            threading.Timer(task.store['interval'], self._executeTiming,args=[task,starSign,executeNum]).start()
    def _executeImmediately(self,functions,options={}):
        if self._judgeFunction(functions) == 'method' or self._judgeFunction(functions) == 'function':
            self.q.put((functions,options))
        elif self._judgeFunction(functions) == 'list':
            for i in range(len(functions)):
                self.q.put((functions[i],options))
    def _judgeFunction(self,functions):
        if isinstance(functions, MethodType):
            return "method"
        elif type([]) == type(functions):
            return "list"
        elif isinstance(functions, FunctionType):
            return "function"
        return None
    def  clearTimingTask(self,taskName):#清除正在计时的任务。
        self.getExecuteTask(taskName).store['clear']=True

    def putExecuteList(self,executeList,mode='1'):
        """
        立即执行
        定时执行
        循环执行
        """
        pass
    def _emptyWork(self):
        def f():
            pass
        self.q.put((f,{}))
    def close(self):
        #清除所有的计时器任务
        for key in self.executeTasks.keys():
            if  self.executeTasks[key].store['isExecute']:
                self.clearTimingTask(key)
        # self.clearTimingTask()
        self.sign=-1
        self._emptyWork()
    def getExecuteLog(self):
        return self.log
class Task:
    """
    1.方法
    2.参数
    3.模式=立即执行，延时执行，循环延时执行
    4.
    """
    def __init__(self,functionsAndOptions=[],mode="",interval=1,executeNum=-1):

        self.store={
            'mode':mode,
            'functionsAndOptions':functionsAndOptions,
            'interval':interval,
            'executeNum':executeNum,
            'clear':False,
            'isExecute':False#标识
        }
        self.modes=['immediately','Timing']
        # self.name=name
        # self.functionsAndOptions=functionsAndOptions
        # self.mode=mode
        # self.interval=interval
        # self.executeNum=executeNum
        # self.starSign=0
        if JudgeType.getType(self.store['functionsAndOptions'])=='method' or JudgeType.getType(self.store['functionsAndOptions'])=='function':
            self.store['functionsAndOptions']=[(functionsAndOptions,{})]
        if type([]) != type(self.store['functionsAndOptions']):
            self.store['functionsAndOptions'] = [functionsAndOptions]
        for i in range(len(self.store['functionsAndOptions'])):
            if JudgeType.getType(self.store['functionsAndOptions'][i])=='method' or JudgeType.getType(self.store['functionsAndOptions'][i])=='function':
                self.store['functionsAndOptions'][i]=(self.store['functionsAndOptions'][i],{})
            elif type(self.store['functionsAndOptions'][i])==type((0,0)):
                pass
            else:
                raise ValueError("参数functionsAndOptions类型出现错误，只能是method，function，tuple，array这几个类型组合成的array类型"+self.store['functionsAndOptions'][i])
            # self.functionsAndOptions=[functionsAndOptions]


    pass
if __name__ == '__main__':
    def run(name='张三',age=222,a=[]):
        print("我是"+name+"今年"+str(age))
        print("我是" + name + "今年" + str(age))
        print(type(a))
    a = Engine()
    a.start()
    a.setExecuteTask(name='11',task=Task(mode='Timing',interval=1,executeNum=-1,functionsAndOptions=[(run,{'name':'李四','age':1})]))
    a.execute('11')

    # a.clearTimingTask('11')
    # time.sleep(5)
    a.close()

