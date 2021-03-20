from functools import reduce
from _xhr_tool.phoneRobot import Device


if __name__ == '__main__':
    arr=[{'公司名称':'张三'},{'公司名称':'李四'},{'公司名称':'张三'}]
    def test(x,y):
        for x1 in x:
            if x1['公司名称']==y['公司名称']:
                return x
        return x+[y]
    arr=reduce(test,[[], ] + arr)
    print(arr)


