from queue import Queue
from _xhr_tool.chromeRobot.src._abstract_class.engine import ObjsPool_abstract


class ObjsPool(ObjsPool_abstract):

    def __init__(self,obj_class,args=[],kwargs={},initNum=10,addNum=10):
        """
        在子类的__init__方法中必须传入obj_class。
         super().__init__(类名,num=10)
        :param obj_class:
        :param args:
        :param num:
        """
        self.pool = Queue()
        self._obj_class = obj_class
        self._initNum=initNum
        self._addNum=addNum
        self._args=args
        self._kwargs=kwargs
        self._poolAdd(initNum)

    def _poolAdd(self,num=10):
        for i in range(num):
            self.pool.put(self._obj_class(*self._args,**self._kwargs))

    def get(self):
        if self.pool.qsize()==0:
            self._poolAdd(num=self._addNum)
        return self.pool.get(block=False)

    def back(self,obj):
        if type(obj)!=self._obj_class:
            raise TypeError('归还对象类型错误:该类型:'+str(type(obj))+'与初始化的类型:'+str(self._obj_class)+'类型不一致')
        self.pool.put(obj)
