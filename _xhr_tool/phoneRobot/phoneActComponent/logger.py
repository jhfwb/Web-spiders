# 用于将数据记录以及打印。
from _xhr_tool._utils.RUtils import tool

def log(func):
    """
    当拥有该注解的方法，拥有以下特性。
    当该方法的参数有note的时候，则会在屏幕中打印note
    """
    def log1(*args, **kwargs):
        if kwargs.get('note')!=None:
            tool().print(kwargs.get('note'))
            kwargs.pop('note')
        return func(*args, **kwargs)
    return log1 # 返回需要执行的新的方法
