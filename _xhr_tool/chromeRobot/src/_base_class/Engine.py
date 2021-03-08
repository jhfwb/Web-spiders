import abc
import inspect
import threading
import time
from _xhr_tool._annotate import threadingRun, singleObj
from _xhr_tool.chromeRobot.src._abstract_class.engine import ExcuteEngine_abstract
from _xhr_tool.chromeRobot.src._base_class.Pool import ObjsPool
import importlib
# 元类
# https://blog.csdn.net/weixin_40907382/article/details/79564209?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.control&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.control



@singleObj
class ExcuteEngine(ExcuteEngine_abstract):
    _excuteList=[]
    _cacheList=[]
    _condition=threading.Condition()
    """执行队列,本质是一个list，从头部开始执行，执行到末尾"""
    state='unexecuted'or 'excuting' or 'wait'#1.执行中 2.等待执行中（阻塞） 3.未启动=0
    """1.excuting执行中 2.wait等待执行中（阻塞） 3.unexecuted未启动"""
    def __init__(self):
        self._excuteFuelPool=ExcuteFuelPool()#初始化线程池
    @threadingRun
    def run(self):
        while True:
            self.excute()
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
        self.put_excuteFuels(fuels=self._cacheList,excuteOrder=excuteOrder)
        self._cacheList=[]#清空缓存版内容
    def getNewFuel(self):
        # type:()->ExcuteFuel
        return self._excuteFuelPool.get()
    def backFuel(self,fuel):
        self._excuteFuelPool.back(fuel)

    def put_excuteFuel(self,fuel,excuteOrder='last' or 'first' ): #在执行队列
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
            self._excuteList.append(fuel)
        elif excuteOrder=='first':
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
    def beforeExcute(self,fuel):
        """
        此方法无需调用,只用来覆写。在执行的时候，会先执行该方法。
        :param fuel:
        :return:
        """
        
        pass
    def afterExcute(self,fuel):
        pass
    def excute(self):#执行方法
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
        self.beforeExcute(fuel)
        before_result=None
        if fuel.get_before_func()!=None:
            before_result=fuel.get_before_func()(*fuel.get_before_func_args(),**fuel.get_before_func_kwargs())
            if type(before_result)!=bool:
                raise TypeError('类型错误:前置函数必须是bool类型。')
        if before_result==True or before_result==None:
            result=fuel.get_func()(*fuel.get_func_args(),**fuel.get_func_kwargs())
        if fuel.get_after_func()!=None:
            fuel.get_after_func()(result,*fuel.get_after_func_args(),**fuel.get_after_func_kwargs())
        self.afterExcute(fuel)
        ExcuteFuelPool().back(fuel)#执行完毕，归还
        self._condition.release()
    def stop(self):
        pass
    def start(self):
        self.state='excuting'
        self.run()
    def close(self):
        pass
class Interceptor:
    def handle(self,fuel):
        # 导入模块

        mod = importlib.import_module('_xhr_tool.chromeRobot.src._base_class.testtt')
        classes=inspect.getmembers(mod, inspect.isclass)
        for cls in classes:
            if cls[1].__base__.__name__==Interceptor.__name__:
                print(cls[1])

        # print(classes)
        # cls = getattr(mod, clsname)
        # print(cls)
        # print(cls.__subclasses__())
        interceptorClasses= [subsclass for subsclass in Interceptor.__subclasses__()]
        # print(interceptorClasses)
        for interceptorClass in interceptorClasses:
            interceptorClass().haha()
    @abc.abstractmethod
    def haha(self):
        pass
class 自定义拦截器(Interceptor):
    pass

class 自定义拦截器3(Interceptor):
    pass
    # def haha(self):
    #     print('你好')

class ExcuteFuel:
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
    _meta={}
    _before_func_result=None
    _func_result=None
    _after_func_result=None
    def __init__(self,func=None,func_args=[],func_kwargs={},
                 before_func=None,before_func_args=[],before_func_kwargs={},
                 after_func=None,after_func_args=[],after_func_kwargs={}):
        self.setFuel(func=func,func_args=func_args,func_kwargs=func_kwargs,
                     before_func=before_func,before_func_args=before_func_args,before_func_kwargs=before_func_kwargs,
                     after_func=after_func,after_func_args=after_func_args,after_func_kwargs=after_func_kwargs)
    def setFuel(self,func=None,func_args=[],func_kwargs={},
                before_func=None,before_func_args=[],before_func_kwargs={},
                after_func=None,after_func_args=[],after_func_kwargs={},
                func_result=None,before_func_result=None,after_func_result=None):
        self._func=func
        self._func_args=func_args
        self._func_kwargs=func_kwargs

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
    def get_meta(self):
        return self._meta
    def get_func(self):
        return self._func
    def get_func_args(self):
        return self._func_args
    def get_func_kwargs(self):
        return self._func_kwargs

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
        if len(self._func_args) != 0:
            s=s+',func_args:'+str(self._func_args)
        if len(self._func_kwargs) != 0:
            s=s+',func_kwargs:'+str(self._func_kwargs)


        if self._before_func != None:
            s = s + ',before_func:'+self._before_func.__name__
        if len(self._before_func_args )!= 0:
            s = s + ',before_func_args:' + str(self._before_func_kwargs)
        if len(self._before_func_kwargs) != 0:
            s = s + ',before_func_kwargs:' + str(self._before_func_kwargs)

        if self._after_func != None:
            s = s + ',after_func'+self._after_func.__name__
        if len(self._after_func_args )!= 0:
            s = s + ',after_func_args:' + str(self._after_func_args)
        if len(self._after_func_kwargs) != 0:
            s = s + ',after_func_kwargs:' + str(self._after_func_kwargs)

        if self._before_func_result!=None:
            s = s + ',before_func_result:' + str(self._before_func_result)
        if self._func_result !=None:
            s = s + ',func_result:' + str(self._func_result)
        if self._after_func_result!=None:
            s = s + ',after_func_result:' + str(self._after_func_result)

        return "Excute_fuel(id="+str(id(self))+")"+s+",'excuteEngine':[...]}"
class ExcuteFuelPool(ObjsPool):
    def __init__(self):
        super().__init__(obj_class=ExcuteFuel)  # 调用父类的方法，初始化10个ExcuteFuel
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
    e=ExcuteEngine()
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