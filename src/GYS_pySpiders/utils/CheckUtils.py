import time
import inspect as ist

class CheckUtils:
    @staticmethod
    def checkObje(arr,sleepTime=0,stop=False):
        """
        arg:
        arr  需要检查的object数组
        sleepTime  检查完成后，线程休眠时间。默认为0
        stop  检查完后，是否发出异常中断该线程。默认为false

        e.g.
        CheckUtils.checkObje([cls, crawler,s], sleepTime=10,stop=True)
        """
        for next in arr:
            print("↓----------------------------↓")
            print("对象:"+str(next))
            print("对象类型:"+str(type(next)))
            print("对象属性:"+str(dir(next)))
            print("↑----------------------------↑")
        CheckUtils.stop(sleepTime,stop)

    @staticmethod
    def stop(sleepTime=0,stop=False):
        time.sleep(sleepTime)
        if stop:
            raise ValueError("检查截止！！！！！！！已经中断该线程！！！！！！")
    @staticmethod
    def getCode(obj,sleepTime=0,stop=False):
        """
        获得obj的源代码
        e.g.
        CheckUtils.getCode(crawler.signals.connect,sleepTime=10,stop=True)

        """
        print("↓----------------------------↓")
        print("对象:"+str(obj))
        c = ist.getsource(obj)
        print(c)
        print("↑----------------------------↑")
        CheckUtils.stop(sleepTime, stop)