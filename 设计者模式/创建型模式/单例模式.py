class Singleton(object):
    """
    单例模式：
    确保一个对象只有一个内存地址。无论在哪个地方，当创建新对象的时候，确保还是原来那个对象。
    """
    def __init__(self):
     pass

    def __new__(cls, *args, **kwargs):
     if not hasattr(Singleton, "_instance"): # 反射
         Singleton._instance = object.__new__(cls)#创建新对象的一个api方法
     return Singleton._instance
    def pri(self):
        pass

obj1 = Singleton()
print(dir(obj1))
obj2 = Singleton()
obj1.pri()
# print(dir(obj2))
# print(obj1, obj2) #<__main__.Singleton object at 0x004415F0> <__main__.Singleton object at 0x004415F0>