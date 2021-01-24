import os
import sys
# https://blog.csdn.net/u010358168/article/details/77773199
def inner_workpathLock(innerWorkPath=""):
    """
    设置方法内部的工作路径。当离开该方法后，工作路径恢复原来的工作路径
    --该注释的目的是为了防止入口函数的变换导致相对路径的偏移。
    """
    def inner(func):
        def run(*args,**kwargs):
            path=os.getcwd()
            os.chdir(innerWorkPath)
            func(*args,**kwargs)
            os.chdir(path)
        return run
    return inner

@inner_workpathLock(innerWorkPath='c://')
def test():
    print(os.getcwd())
    pass

if __name__ == '__main__':
    test()