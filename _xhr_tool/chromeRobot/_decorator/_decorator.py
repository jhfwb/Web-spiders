from types import FunctionType

from _xhr_tool._utils import reflexUtils
def chrome_robot_excute(times=1):
    """执行谷歌方法
    eg:
        >>>@chrome_robot_excute(times=3)#执行3次
        >>>def test():
        ...

    """
    if isinstance(times, FunctionType):
        func=times
        def run(*args, **kwargs):
            func(*args, **kwargs)
        return run
    def run2(func):
        def run1(*args,**kwargs):
            for i in range(times):
                func(*args,**kwargs)
        return run1
    return run2

    # if len(crg)==0:
    #     def run3(func):
    #         def run2(*args, **kwargs):
    #             func(*args, **kwargs)
    #         return run2
    #     return run3
    # else:
    #
    #     if isinstance(crg[0],FunctionType):
    #         def run2(*args, **kwargs):
    #             crg[0](*args, **kwargs)
    #         return run2
    #     else:
    #         def run1(func):
    #             print(crg)
    #             def run(*args,**kwargs):
    #                 func(*args,**kwargs)
    #             return run
    #         return run1

def chrome_datas_catch(func):
    def run(*args, **kwargs):
        func(*args, **kwargs)
    return run