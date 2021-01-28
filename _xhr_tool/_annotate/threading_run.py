# 用于多线程
import threading
def threadingRun(func):
    """
    多线程装饰器，能够快速实现方法的多线程。
    """
    def run(*args, **kwargs):
        return threading.Thread(target=func, args=args, kwargs= kwargs).start()
    return run # 返回需要执行的新的方法
@threadingRun
def _test(c,a,b=1):
    while True:
        pass
    return 1
if __name__ == '__main__':
    print(_test('1','2',b='3'))
    print(22)