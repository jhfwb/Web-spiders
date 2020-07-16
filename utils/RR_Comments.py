import os
import re
import sys
import time


class PrintTool:
    """
    存放打印工具。
    """
    @staticmethod
    def print(s,fontColor='red',backgroundColor='white',displayWay=0):
        """
        默认字体为红色。背景色为白色
        能够按照颜色在控制台打印出来。可以自定义背景色和字体颜色。下划线等

        :param s:打印的内容
        :param fontColor: (str) red | green | yellow  | pink  | blue| gray | black
        :param backgroundColor: (str) red | green | yellow | blue  | black
        :param displayWay: (int) 0 普通模式 |
                                 1 字体加粗 |
                                 4 下划线 |
        :return: None
        """
        s = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+" | " + s
        fontColorArr=[('red',31),('green',32),('yellow',33),('pink',35),('blue',34),('gray',37),('black',30)]
        backgroundColorArr=[('red',41),('green',42),('yellow',43),('blue',44),('black',40),('pink',45),('gray',47)]
        backgroundColorNUM = "init"
        fontColorNUM='init'
        for fontColor1 in fontColorArr:
            if fontColor1[0]==fontColor:
                fontColorNUM=fontColor1[1]
                break
        for backgroundColorArr1 in backgroundColorArr:
            if backgroundColorArr1[0]==backgroundColor:
                backgroundColorNUM = backgroundColorArr1[1]
                break
        if type(fontColorNUM)!=type(0) :
            raise ValueError("传入的fontColor有问题！找不到该字体颜色"+fontColor)
        if type(backgroundColorNUM)!=type(0) and backgroundColor!="white":
            raise ValueError("传入的backgroundColorNUM有问题！找不到该背景颜色" + backgroundColor)
        if displayWay==2:
            displayWay=4
        line="------------FILE:"+str(sys._getframe(1).f_code.co_filename)+"_____MODULE:"+str(sys._getframe(1).f_code.co_name)+"_____LINE:"+str(sys._getframe(1).f_lineno)
        if backgroundColor=="white":
            print('\033['+str(displayWay)+';' + str(fontColorNUM) + 'm', s,line)
        else:
            print('\033['+str(displayWay)+';'+str(fontColorNUM) + ';' + str(backgroundColorNUM) + 'm', s,line)
        print('\033[0m',end="")
class ArrTool:
    @staticmethod
    def removeRepeat(arr, keyFunction=""):
        """
        去除掉[]中相同的元素，根据方法keyFunction。
        e.g.:a=[{'name':1},{'name':3},{'name':2},{'name':1},{'name':1}]
        假设要去除name为1的元素
        c=removeRepeat(a,keyFunction=lambda x:x['name'])
        print(c) =>[{'name': 1}, {'name': 2}, {'name': 3}]

        @param:arr |[] 需要去重的数组
        @param:keyFunction |function 存放需要进行去重的函数
        """
        try:
            arr.sort(key=keyFunction)
        except:
            raise ValueError("keyFunction无法正常调用,请确保数组arr中的每个元素都能够执行keyFunction方法,并且不会报错。arr:"+str(arr))
        mid = None
        for i in range(len(arr)):
            if mid != arr[i]:
                mid = arr[i]
            else:
                arr[i] = None
        return list(filter(lambda x: x != None, arr))
class JudgeType:
    #判断类是什么类型
    #核心方法是type()
    #返回方法的名称
    #dict：字典类型
    @staticmethod
    def getType(obj):
        """
        判断类型：
        目前可以判断的类型如下：
            dict
            int
            str
            blo
            list
            method
            function
            module
            other：obj
        :param obj:
        :return:
        """
        if type(obj)==type({}):
           return "dict"
        if type(obj)==type(1):
           return "int"
        if type(obj)==type(""):
            return "str"
        if type(obj)==type(True):
            return "blo"
        if type(obj)==type([]):
            return "list"
        #if type(obj)==type():
        else:
            s = str(obj)
            if len(re.findall('<.*at.*>', s)) != 0:
                if len(re.findall('method', s)) != 0:
                    return 'method'
                elif len(re.findall('function', s)) != 0:
                    return 'function'
                elif len(re.findall('module', s)) != 0:
                    return 'module'
                else:
                    return 'obj'
        return None
class ReflexTool:
    @staticmethod
    def execute(function="", options={},pyFilePath='',className='',initObjectOptions={}):
        """
        用反射的机制去运行方法。
        @param: function |function or method
        @param: option | dict
        """
        if function=="":
            raise ValueError("function为空")
        if type(function) == type(""):
            function = ReflexTool.getObjectMethod(filePath=pyFilePath, className=className, methodName=function,
                                                  initObjectOptions=initObjectOptions)
        if len(options) == 0:
            return function()
        else:
            keys = options.keys()
            argStr = ""
            for key in keys:
                if type(options[key]) == type(-1):
                    argStr += key + "=" + str(options[key]) + ","
                elif type(options[key]) == type(""):
                    argStr += key + "='" + options[key] + "',"
                else:
                    argStr += key + "=" + str(options[key]) + ","
            argStr = argStr[0:len(argStr) - 1]
            return eval("function(" + argStr + ")")

    @staticmethod
    def newInstance(filePath='',className="",options={}):
        classn=ReflexTool.getClass(filePath,className)
        if len(options) == 0:
            return classn()
        else:
            keys = options.keys()
            argStr = ""
            for key in keys:
                if type(options[key]) == type(-1):
                    argStr += key + "=" + str(options[key]) + ","
                elif type(options[key]) == type(""):
                    argStr += key + "='" + options[key] + "',"
                else:
                    argStr += key + "=" + str(options[key]) + ","
            argStr = argStr[0:len(argStr) - 1]
            return eval("classn(" + argStr + ")")
    @staticmethod
    def getMethod(filePath='',className="",methodName=""):
        classInstance = ReflexTool.getClass(filePath, className)
        try:
            return eval("classInstance."+methodName)
        except:
            raise ValueError("找不到该方法"+methodName)

    @staticmethod
    def getObjectMethod(filePath='', className="", methodName="",initObjectOptions={}):
        classInstance = ReflexTool.newInstance(filePath, className,initObjectOptions)
        try:
            return eval("classInstance." + methodName)
        except:
            raise ValueError("找不到该方法" + methodName)

    @staticmethod
    def getClass(filePath='',className=""):
        a=ReflexTool.getModule(filePath)
        try:
            return eval("a."+className)
        except:
            raise ValueError('找不到该class')
    @staticmethod
    def getModule(pythonFilePath=''):
        """
        导入模块。把该文件夹路径添加到python解释器能够识别的地方。我们称为导入模块
        @param: modulePath | str: 文件夹的路径
        """
        if not pythonFilePath.endswith('.py'):
            raise ValueError("该文件不是py文件：" + pythonFilePath)
        if os.path.exists(pythonFilePath):
            pythonFilePath=pythonFilePath.replace('\\','/')
            index=pythonFilePath.rfind('/')
            sys.path.append(pythonFilePath[0:index])
            exec ("from "+pythonFilePath[pythonFilePath[0:index].rfind('/')+1:index]+" import "+pythonFilePath[index+1:len(pythonFilePath)-3])
            # print("from "+pythonFilePath[pythonFilePath[0:index].rfind('/')+1:index]+" import "+pythonFilePath[index+1:len(pythonFilePath)-3])
            # from Lib import test
            return locals()[pythonFilePath[index+1:len(pythonFilePath)-3]]

        else:
            raise ValueError("该文件不存在"+pythonFilePath)
        return None
import pinyin
class ChinaWordTool:

    @staticmethod
    def getStrAllAplha(str):
        return pinyin.get_initial(str, delimiter="").upper()

    @staticmethod
    def getStrFirstAplha(str):
        str = ChinaWordTool.getStrAllAplha(str)
        str = str[0:1]
        return str.upper()
class StringTool:


    #判断字符串是不是数字。
    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False


if __name__ == "__main__":
    str_input = u'暴风雪3'
    print(ChinaWordTool.multi_get_letter(str_input))
