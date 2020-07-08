from queue import Queue
#ignoreErr 是否无视错误。如果动作出错，则中断后续操作。如果无视了，则继续执行下面的操作

class Action:
    def __init__(self,memo="请输入备注信息"):
        self.acts=Queue()
        pass
    def excute(self,queue):
        queue.put(self.acts)
        return self

    def initWeb(self,memo="正在关闭多余标签...",ignoreErr=False):
        """
        初始化便签。将其他标签关闭。只留下一个标签那
        :return:
        """
        self.acts.put({'way': 'init','memo':memo,'ignoreErr':ignoreErr})#初始化
        return self
    def get(self,web="",memo="",ignoreErr=False):
        """

        :param web: 访问的网站地址
        :return: 返回action丢向
        """
        if memo=="":
            memo="正在访问网址:"+web+"..."
        self.acts.put({'way': 'get',
                            "text": web,'memo':memo,'ignoreErr':ignoreErr
                            })
        return self

    def key_input(self,text="",cssStr="",isClear=True,memo="",ignoreErr=False):
        """
        输入框输入内容
        :param text: 输入框输入的内容，可以输入键值：如Keys.ENTER 则输入回车
        :param cssStr: 输入框的select选择器
        :param isClear:
        :return:
        """
        if memo=="":
            memo="正在为"+cssStr+"输入框输入文字:"+str(text)
        self.acts.put({'way': 'key_input',
                            "css": cssStr,
                            "text": text,
                            "isClear": isClear,'memo':memo,'ignoreErr':ignoreErr})
        return self
    def click(self,cssStr="",memo="",ignoreErr=False,success="",exception=""):
        if memo=="":
            memo="正在点击按钮："+cssStr
        self.acts.put({'way': 'click',
                       "css": cssStr,
                       "memo":memo,
                       'ignoreErr':ignoreErr,
                       'success':success,
                       'exception':exception,
                       'action':self
                            })  # 点
        return self
    def find(self,cssStr="",key="",memo="",ignoreErr=False,mode=""):
        if memo=="":
            memo="正在查找信息"+key+"其选择器为"+cssStr
        self.acts.put({'way': 'find',
                           "css": cssStr,
                           "key": key,
                           "memo":memo,
                           'ignoreErr':ignoreErr,
                            'mode':mode
                       })
        return self


