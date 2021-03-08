import os
import sys
import threading
import time
from selenium.webdriver.support.color import Color, Colors
import os
class tool:
    """
    存放自定义的基础工具包
    """
    _instance = None
    def __init__(self):
        pass
    def __new__(cls, *args, **kwargs):
        if tool._instance==None:
            tool._instance=super().__new__(cls, *args, **kwargs)#调用上级的创建方法。
        return  tool._instance
    @staticmethod
    def bug():
        Colors.pop()
        assert 1/0

    @staticmethod
    def startNewThread(fun):
        t1 = threading.Thread(target=fun, args=[])  # 开始服务器端的监听
        t1.start()
        return t1

    def printColor(self,s="",fontColor='black',end="\n"):
        """打印出有颜色的字体。默认为黑色。打印后返回打印的值。
        :param str s: 需要打印的内容
        :param str fontColor: 颜色可以是以下几种 red | green | yellow | pink | blue | gray | black | cyan
        :param end: 末尾的字符。(一般是\n或者空字符)
        :return: 返回s的值
        """
        glock=threading.Lock()
        glock.acquire()
        fontColorArr = { 'black': 30,'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'pink': 35, 'cyan':36 ,'gray': 37}
        line=str(fontColorArr.get(fontColor))
        if fontColorArr.get(fontColor) == None:
            raise ValueError("传入的fontColor有问题！找不到该字体颜色:" + fontColor)
        print('\033[0;' + line + 'm', s,end=end)
        glock.release()
        return line
    def print(self,s,fontColor='blue',timeStrColor="red",siteColor="pink",path=None):
        """
        默认字体为红色。背景色为白色
        能够按照颜色在控制台打印出来。可以自定义背景色和字体颜色。下划线等
        :param s:打印的内容
        :param fontColor: (str) red | green | yellow  | pink  | blue| gray | black
        :param timeStrColor: (str) red | green | yellow | blue  | black
        :param siteColor: (int) 0 普通模式 |
                                 1 字体加粗 |
                                 4 下划线 |
        :return: None
        """
        # print(sys._getframe(1).f_lineno)
        # print(sys._getframe(1).f_code.co_filename)
        # print(sys._getframe(1).f_code.co_name)
        # print(sys._getframe(1).f_lineno)
        # 1.打印时间
        # 2.打印内容
        # 3.打印位置

        line=""
        # line = "------------FILE:" + str(sys._getframe(1).f_code.co_filename) + "_____MODULE:" + str(
        #     sys._getframe(1).f_code.co_name) + "_____LINE:" + str(sys._getframe(1).f_lineno)

        # 1.打印时间
        self.printColor(s='[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ']',fontColor=timeStrColor,end="")

        # 2.打印内容
        self.printColor(s=s, fontColor=fontColor,
                        end="")
        # print(sys._getframe(1).f_code.co_name)
        # print(sys._getframe(2).f_code.co_name)
        # print(sys._getframe(3).f_code.co_name)
        # print(sys._getframe(4).f_code.co_name)
        line = "------------FILE:" + str(sys._getframe(1).f_code.co_filename) + "_____MODULE:" + str(
            sys._getframe(1).f_code.co_name) + "_____LINE:" + str(sys._getframe(1).f_lineno)
        # 3.打印位置
        self.printColor(s=line,fontColor=siteColor,end="")
        self.printColor()
        if path!=None:
            if os.path.isfile(path):
                pass
            else:
                raise ValueError('保存路径异常:'+str(path)+'.不存在该文件!')

    @staticmethod
    def isBaseType(variate):
        """
        判断该变量是不是基础类型
        :param variate:
        :return:
        """
        type1 = ""
        if type(variate) == type(1):
            type1 = "int"
            return True
        elif type(variate) == type("str"):
            type1 = "str"
            return True
        elif type(variate) == type(12.3):
            type1 = "float"
            return True
        elif type(variate) == type([1]):
            type1 = "list"
            return True
        elif type(variate) == type(()):
            type1 = "tuple"
            return True
        elif type(variate) == type({"key1": "123"}):
            type1 = "dict"
            return True
        elif type(variate) == type({"key1"}):
            type1 = "set"
            return True
        return False

    @staticmethod
    def getType(data):
        """
        获得其数据的类型，目前更新下面两种

        1.json类型 json
        2.文本类型 text
        :param data:
        :return: 上述类型
        """
        data=str(data)
        if data.startswith('{')&data.endswith("}"):
            try:
                data=eval(data)
                if type(data)==type({}):
                    return "json"
                else:
                    return "text"
            except:
                return "text"
        else:
            return "text"
if __name__ == '__main__':
    tool().print("你好哦")
    print(222)
    tool().print("你好哦")
    tool().print("你好哦")
    print(111)
    tool().print("你好哦")



