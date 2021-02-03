import inspect
import sys


def getFunctionArgs(func):
    def run(*args,**kwargs):
        # 1.默认赋值
        funcArg=inspect.getfullargspec(func)
        vnames=funcArg.args
        values=funcArg.defaults
        obj={}
        di=len(vnames)-len(values)
        for i in range(len(values)):
            obj.setdefault(vnames[i+di],values[i])
        # 2.参数赋值
        print(*args)

        # 2.
        print(obj)

        # print(func)
        # print(args)
        # print(kwargs)
        _args()
    return run


def _args():  # 对参数进行处理的中间方法
    # print(sys._getframe(1).f_locals)
    # option = vars()
    # option.setdefault('way', )
    # self.acts.put(option)
    pass

