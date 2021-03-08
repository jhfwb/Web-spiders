#encoding=utf8
#http://www.fanjun.me/?p=568
from queue import Queue

from _xhr_tool._annotate import threadingRun


@threadingRun
def test(arr):
    for i in range(100000):
        print(arr.pop())
    print('list执行完毕')
def test2(arr):
    for i in range(100000):
        print(arr.get())
    print('queue执行完毕')
if __name__ == '__main__':
    arr=[]
    arr2=Queue()
    for i in range(100000):
        arr.append(i)
    for i in range(100000):
        arr2.put(i)

    test(arr)
    test2(arr2)

