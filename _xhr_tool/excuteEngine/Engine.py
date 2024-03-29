import abc
import inspect
import threading
import time
from _xhr_tool._annotate import threadingRun, singleObj
from _xhr_tool._utils import relpath
from _xhr_tool._utils.RUtils import tool
from _xhr_tool._utils.xhr_logger import Logger
from _xhr_tool.chromeRobot.src._abstract_class.engine import ExcuteEngine_abstract
from _xhr_tool.chromeRobot.src._base_class.Pool import ObjsPool
import importlib
# 元类
# 错误等级:重新执行方法，重新执行
# https://blog.csdn.net/weixin_40907382/article/details/79564209?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.control
from _xhr_tool.excuteEngine.Component import ExcuteInterceptor, Interceptor, PutExcuteFuelInterceptor, \
    BackFuelInterceptor
from _xhr_tool.excuteEngine.Interceptors import LogInterceptor
import configparser
class ExcuteEngine(ExcuteEngine_abstract):
    _state=0 or 1 or 2 or 3 #1.未启动  2.等待执行  3.执行中

    _historyExcuteList=[]#历史执行记录表，末尾的数据为最新数据
    _excuteList=[] #执行栈。头部的方法先执行，尾部的方法后执行。
    _cacheList=[]
    _condition=threading.Condition()
    #拦截器组
    _excute_interceptors=[]
    _putExcuteFuel_interceptors=[]
    _backFuel_interceptors=[]
    _config=None
    """执行队列,本质是一个list，从头部开始执行，执行到末尾"""
    state='unexecuted'or 'excuting' or 'wait'#1.执行中 2.等待执行中（阻塞） 3.未启动=0
    """1.excuting执行中 2.wait等待执行中（阻塞） 3.unexecuted未启动"""
    def __init__(self,historyExcuteNum=10,configFiltPath='',erro=''):
        #当出现错误的时候,会有不同的应对方式，1.不做应对，抛出异常。2.重新执行此方法。3.清空执行栈的方法
        self._historyExcuteNum=historyExcuteNum
        self._excuteFuelPool=ExcuteFuelPool(excuteEngine=self)#初始化线程池
        self._initInterceptors()
        #初始化配置信息
        # self._initConfig(configFiltPath)
        #初始化日记系统
        # self._logger=Logger(savePath=self._config['logger']['savePath'])
    def _initConfig(self,configFiltPath):
        if configFiltPath=='':
            configFiltPath=relpath('config.ini')
        config = configparser.ConfigParser()
        config.read(filenames=configFiltPath)
        self._config = config

    def _initInterceptors(self):
        self.registerInterceptors(LogInterceptor)

    def registerInterceptors(self,*interceptors):
        """
        :param interceptors: 类的类型即可，不可传入实例。
        :return:
        """
        for interceptor in interceptors:
            try:
                if interceptor.__base__.__base__!=Interceptor:
                    raise ValueError('注册拦截器失败:该拦截器:'+str(interceptor)+'，类型错误。不是interceptor类型')
            except AttributeError:
                raise ValueError('注册拦截器失败:该拦截器:'+str(interceptor)+'，错误，请传入一个类，而非一个对象。')
            #判断拦截器的类型，然后装入合适的地方
            interceptor.engine=self
            if interceptor.__base__==ExcuteInterceptor:
                self._excute_interceptors.append(interceptor())
            if interceptor.__base__==PutExcuteFuelInterceptor:
                self._putExcuteFuel_interceptors.append(interceptor())
            if interceptor.__base__==BackFuelInterceptor:
                self._backFuel_interceptors.append(interceptor())
    @threadingRun
    def run(self):
        while True:
            self._excute()
    #注册打断器
    #将放入缓冲板中
    def put_excuteFuelCache(self,fuels=[],excuteOrder='last' or 'first'):
        if excuteOrder == 'last':
            for fuel in fuels:
                self._cacheList.append(fuel)
        elif excuteOrder == 'first':
            for i in range(len(fuels)):
                self._cacheList.insert(0,fuels.pop())
        else:
            raise ValueError('未知参数excuteOrder:' + excuteOrder + ';只允许excuteOrder为last或者first')
    #执行缓冲板中的内容 要先执行还是后执行，由自己决定
    def excuteFuelCache(self,excuteOrder='last' or 'first'):
        #阻塞,当执行栈为空的时候，才会执行该方法。
        self.put_excuteFuels(fuels=self._cacheList,excuteOrder=excuteOrder)
        self._cacheList=[]#清空缓存版内容
    def getNewFuel(self):
        # type:()->ExcuteFuel
        return self._excuteFuelPool.get()
    def backFuel(self,fuel):
        self._excuteFuelPool.back(fuel)
    def clear_excuteList(self):#清空执行栈。
        self._excuteList.clear()
        pass
    def put_excuteFuel(self,fuel,excuteOrder='last' or 'first'): #在执行队列
        """
        将方法与参数存入执行栈中，准备执行。该fuel，放在执行栈末尾，前面执行完毕后再执行
        :param ExcuteFuel fuel: 执行燃料；内部存放需要执行的方法，以及该方法的参数
        :param excuteOrder: 执行顺序，将该方法放在执行首位或者末尾
        :return:
        """
        if self.state == 'wait':
            self._condition.acquire()
            self._condition.notify()
            self._condition.release()
        if excuteOrder=='last':
            for intercept in self._putExcuteFuel_interceptors:
                intercept.intercept_before_put(fuel)
            self._excuteList.append(fuel)
        elif excuteOrder=='first':
            for intercept in self._putExcuteFuel_interceptors:
                intercept.intercept_before_put(fuel)
            self._excuteList.insert(0, fuel)
        else:
            raise ValueError('未知参数excuteOrder:'+excuteOrder+';只允许excuteOrder为last或者first')
    def put_excuteFuels(self,fuels=[],excuteOrder='last' or 'first' ):
        """
        放入excuteFuels的数组，注意。该方法
        :param fuels:
        :return:
        """
        if excuteOrder=='last':
            for fuel in fuels:
                self.put_excuteFuel(fuel,excuteOrder)
        elif excuteOrder=='first':
            for i in range(len(fuels)):
                self.put_excuteFuel(fuels.pop(),excuteOrder)
        else:
            raise ValueError('未知参数excuteOrder:'+excuteOrder+';只允许excuteOrder为last或者first')
    def block(self,timeOut=-1):
        if timeOut < 0:
            while True:
                if self.state=='wait' and len(self._excuteList)==0:
                    break
                time.sleep(1)
        else:
            while True:
                timeOut=timeOut-1
                if self.state=='wait' and len(self._excuteList)==0:
                    break
                if timeOut<0:
                    break
                time.sleep(1)
    def excuteFuel(self,fuel):
        """
        取出执行栈中的数据。然后执行该数据。
        :return:
        """
        for interceptor in self._excute_interceptors:
            interceptor.intercept_before_excute(fuel)
        before_result = None
        result = None
        if fuel.get_before_func() != None:
            before_result = fuel.get_before_func()(*fuel.get_before_func_args(), **fuel.get_before_func_kwargs())
            fuel.set_before_func_result(before_result)
            if type(before_result) != bool:
                raise TypeError('类型错误:前置函数必须是bool类型。')
        if (before_result == True or before_result == None) and fuel.get_func() != None:
            try:
                result = fuel.get_func()(*fuel.get_func_args(), **fuel.get_func_kwargs())
            except Exception:
                raise Exception('ExcuteEngine_Err:运行错误_:方法:'+str(fuel.get_func().__name__)+'|普通参数:'+str(fuel.get_func_args())+',关键字参数:'+str(fuel.get_func_kwargs()))

            fuel.set_func_result(result)
        if result:
            if fuel.get_after_func() != None:
                after_result = fuel.get_after_func()(result, *fuel.get_after_func_args(),
                                                     **fuel.get_after_func_kwargs())
                fuel.set_after_func_result(after_result)
        for interceptor in self._excute_interceptors:
            interceptor.intercept_after_excute(fuel)
        return fuel
        # 执行完毕，归还
    def _excute(self):
        self._condition.acquire()
        if len(self._excuteList)==0:
            self.state='wait'
            # tool().print('-----ExcuteEngine:excute waitting!!!-----')
            self._condition.wait()
            self.state='excuting'
        fuel: ExcuteFuel = self._excuteList.pop(0)
        self.excuteFuel(fuel)
        # 引入一个执行池
        self._historyExcuteList.insert(0, fuel)
        if len(self._historyExcuteList) > self._historyExcuteNum:
            needBackFuel = self._historyExcuteList.pop()
            for interceptor in self._backFuel_interceptors:
                interceptor.intercept_before_backFuel(needBackFuel)
            ExcuteFuelPool().back(needBackFuel)
            for interceptor in self._backFuel_interceptors:
                interceptor.intercept_after_backFuel(needBackFuel)

    def ___excute(self):#执行方法
        """
        取出执行栈中的数据。然后执行该数据。
        :return:
        """
        self._condition.acquire()
        if len(self._excuteList)==0:
            self.state='wait'
            self._condition.wait()
            self.state='excuting'
        fuel:ExcuteFuel=self._excuteList.pop(0)
        for interceptor in self._excute_interceptors:
            interceptor.intercept_before_excute(fuel)
        before_result=None
        result=None
        if fuel.get_before_func()!=None:
            before_result=fuel.get_before_func()(*fuel.get_before_func_args(),**fuel.get_before_func_kwargs())
            fuel.set_before_func_result(before_result)
            if type(before_result)!=bool:
                raise TypeError('类型错误:前置函数必须是bool类型。')
        if (before_result==True or before_result==None) and fuel.get_func()!=None:
            result=fuel.get_func()(*fuel.get_func_args(),**fuel.get_func_kwargs())
            fuel.set_func_result(result)
        if result:
            if fuel.get_after_func()!=None:
                after_result=fuel.get_after_func()(result,*fuel.get_after_func_args(),**fuel.get_after_func_kwargs())
                fuel.set_after_func_result(after_result)
        for interceptor in self._excute_interceptors:
            interceptor.intercept_after_excute(fuel)
        #引入一个执行池
        self._historyExcuteList.insert(0,fuel)
        if len(self._historyExcuteList)>self._historyExcuteNum:
            needBackFuel= self._historyExcuteList.pop()
            for interceptor in self._backFuel_interceptors:
                interceptor.intercept_before_backFuel(needBackFuel)
            ExcuteFuelPool().back(needBackFuel)
            for interceptor in self._backFuel_interceptors:
                interceptor.intercept_after_backFuel(needBackFuel)
        #执行完毕，归还
        self._condition.release()
    def getHistoryExcuteList(self):
        """
        返回历史执行列表的复制。
        该列表从前往后 时间递增。
        :return: list
        """
        return self._historyExcuteList.copy()
    def stop(self):
        pass
    def start(self):
        self.state='excuting'
        self.run()
    def close(self):
        pass

    # def haha(self):
    #     print('你好')

class ExcuteFuel:
    block=False
    """该方法执行的时候是否阻塞"""
    _meta={}
    excuteEngine=None
    _func=None
    _func_args=[]
    _func_kwargs={}
    _before_func=None
    _before_func_args=[]
    _before_func_kwargs={}
    _after_func=None
    _after_func_args = []
    _after_func_kwargs = {}
    _before_func_result=None
    _func_result=None
    _after_func_result=None
    def __init__(self,func=None,func_args=[],func_kwargs={},
                 before_func=None,before_func_args=[],before_func_kwargs={},
                 after_func=None,after_func_args=[],after_func_kwargs={},excuteEngine=None):
        self.excuteEngine=excuteEngine
        self.setFuel(func=func,func_args=func_args,func_kwargs=func_kwargs,
                     before_func=before_func,before_func_args=before_func_args,before_func_kwargs=before_func_kwargs,
                     after_func=after_func,after_func_args=after_func_args,after_func_kwargs=after_func_kwargs)
    def setFuel(self,func=None,func_args=[],func_kwargs={},
                before_func=None,before_func_args=[],before_func_kwargs={},
                after_func=None,after_func_args=[],after_func_kwargs={},
                func_result=None,before_func_result=None,after_func_result=None,meta={}):
        self._func=func
        self._func_args=func_args
        self._func_kwargs=func_kwargs
        self._meta=meta
        self._before_func=before_func
        self._before_func_args=before_func_args
        self._before_func_kwargs=before_func_kwargs
        self._after_func=after_func
        self._after_func_args=after_func_args
        self._after_func_kwargs=after_func_kwargs
        self._func_result=func_result
        self._before_func_result=before_func_result
        self._after_func_result=after_func_result
        return self
    def set_before_func(self,before_func):
        self._before_func=before_func
    def set_func_result(self,func_result):
        self._func_result=func_result
    def set_before_func_result(self,before_func_result):
        self._before_func_result=before_func_result
    def set_after_func_result(self,after_func_result):
        self._after_func_result=after_func_result
    def get_func_result(self):
        return self._func_result
    def get_before_func_result(self):
        return self._before_func_result
    def get_after_func_result(self):
        return self._after_func_result
    def get_func(self):
        return self._func
    def get_func_args(self):
        return self._func_args
    def get_func_kwargs(self):
        return self._func_kwargs
    def get_meta(self):
        return self._meta
    def get_before_func(self):
        return self._before_func
    def get_before_func_args(self):
        return self._before_func_args
    def get_before_func_kwargs(self):
        return self._before_func_kwargs
    def get_after_func(self):
        return self._after_func
    def get_after_func_args(self):
        return self._after_func_args
    def get_after_func_kwargs(self):
        return self._after_func_kwargs

    def __str__(self):
        s="{"
        if self._func != None:
            s=s+'func:'+self._func.__name__
        if self._func_args!=None and len(self._func_args) != 0:
            s=s+',func_args:'+str(self._func_args)
        if len(self._func_kwargs) != 0:
            s=s+',func_kwargs:'+str(self._func_kwargs)
        if self._before_func != None:
            s = s + ',before_func:'+self._before_func.__name__
        if self._before_func_args!=None and len(self._before_func_args )!= 0:
            s = s + ',before_func_args:' + str(self._before_func_kwargs)
        if self._before_func_kwargs!=None:
            if len(self._before_func_kwargs) != 0:
                s = s + ',before_func_kwargs:' + str(self._before_func_kwargs)
        if self._after_func != None:
            s = s + ',after_func'+self._after_func.__name__
        if self._after_func_args != None and len(self._after_func_args )!= 0:
                s = s + ',after_func_args:' + str(self._after_func_args)
        if len(self._after_func_kwargs) != 0:
            s = s + ',after_func_kwargs:' + str(self._after_func_kwargs)
        if self._before_func_result!=None:
            s = s + ',before_func_result:' + str(self._before_func_result)
        if self._func_result !=None:
            s = s + ',func_result:' + str(self._func_result)
        if self._after_func_result!=None:
            s = s + ',after_func_result:' + str(self._after_func_result)
        if self._meta!={}:
            s = s + ',meta:' + str(self._meta)

        return "Excute_fuel(id="+str(id(self))+")"+s+",'excuteEngine':[...]}"
class ExcuteFuelPool(ObjsPool):
    def __init__(self,excuteEngine=None):
        super().__init__(obj_class=ExcuteFuel,kwargs={'excuteEngine':excuteEngine})  # 调用父类的方法，初始化10个ExcuteFuel
    def back(self,fuel:ExcuteFuel):
        super().back(fuel.setFuel())
    def get(self):
        # type:()->ExcuteFuel
        return super().get()
if __name__ == '__main__':
    def test(a,tim='你好我是tim'):
        print('我是测试方法',a,tim)
        return '我是测试方法'
    def test_befo():
        return  False
    class response(ExcuteInterceptor):
        def intercept_before_excute(self, fuel):
            print('执行前')
            pass
        def intercept_after_excute(self, fuel):
            # 导入模块
            pass
    e=ExcuteEngine()
    e.registerInterceptors(response)
    e.put_excuteFuels(fuels=[e.getNewFuel().setFuel(func=test,func_args=['我是大尾巴1'],func_kwargs={'tim':'啊啊啊啊'},before_func=test_befo),
                             e.getNewFuel().setFuel(func=test, func_args=['我是大尾巴2'],)
                             ])
    e.put_excuteFuels(fuels=[e.getNewFuel().setFuel(func=test, func_args=['我是小尾巴1'], before_func=test_befo),
                             e.getNewFuel().setFuel(func=test, func_args=['我是小尾巴2'], before_func=test_befo)

                             ],excuteOrder='first')
    e.start()
    time.sleep(2)
    e.put_excuteFuels(fuels=[e.getNewFuel().setFuel(func=test, func_args=['我是小尾巴31'], before_func=test_befo),
                             e.getNewFuel().setFuel(func=test, func_args=['我是小尾巴32'], before_func=test_befo)
                             ], excuteOrder='first')