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
def chrome_datas_catch(func):
    def run(*args, **kwargs):
        func(*args, **kwargs)
    return run