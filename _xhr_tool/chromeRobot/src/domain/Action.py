import sys
from queue import Queue
#ignoreErr 是否无视错误。如果动作出错，则中断后续操作。如果无视了，则继续执行下面的操作
from _xhr_tool.chromeRobot.src.servlet.robot_thread import MyPipelineThread
class Action:
    """
    注意事项！此处的方法命名必须与web_opeion_methond中的方法一致
    行动。
    # 1. 将方法中的参数变成一个对象。
    # 2. 将对象只行推站处理
    """
    def __init__(self,memo="请输入备注信息",callBackFunc=lambda x:x,packItems=True):
        self.acts=Queue()
        self._bufferActs=[]
        self._callBackFunc=callBackFunc
    def findCurrentUrl(self,key="current_url",catchDate=True,func=lambda x:x,func_args=[],pre_func=lambda x:True,pre_func_args=[]):
        """
        获得当前页面的url
        :return:
        """
        self._args()
        return self
    def connectLastBackFunction(self,func="",func_args=[]):
        """
        连接到上一个方法的回调函数的返回值。该返回值会作为参数传入并传入次此方法。(比较难理解)
        :param func:
        :return:
        """
        self._bufferActs[len(self._bufferActs)-1].setdefault('_sign','connectLastBackFunction')#取出执行栈中的上一个方法。然后添加标记
        # self._bufferActs[len(self._bufferActs)-1].setdefault('_sign_arg',args)#取出执行栈中的上一个方法。然后添加标记
        self._args()
        return self
    def setCallBackFunc(self,callBackFunc):
        self._callBackFunc=callBackFunc
        return self
    def _initAct(self):
        return {
        }
    #实现aop
    def _args(self):#对参数进行处理的中间方法
        methodName=sys._getframe(1).f_code.co_name #获得方法名称
        valueDict=sys._getframe(1).f_locals #获得方法名称
        valueDict.setdefault('way',methodName)
        #添加回调方法
        valueDict.setdefault('way',methodName)
        self._bufferActs.append(valueDict)
    def _before_excute(self,save=False):
        """
        在执行Action之前所进行的动作。
        1.将缓存bufferActs中的动作推入到执行栈中
        :return:
        """
        while len(self._bufferActs)!=0:
            self.acts.put(self._bufferActs.pop(0))
        if save:
            self.acts.put({'way':'save'})
    def excuteActionlater(self):
        self.acts.put(self.buffer)
        self.acts.get()
        MyPipelineThread().readyAction.put(self)
        return self
    def putActionToReadyAct(self,immediately=True,save=False):
        """
        将action放入准备栈中。当该action被执行的时候，会优先执行该方法
        建议每次使用该方法的时候，建议创建一个新的Action
        :return:
        """
        #启动保存

        self._before_excute(save=save)
        if immediately:
            _size=len(MyPipelineThread().readyAct)
            for i in range(self.acts.qsize()):
                MyPipelineThread().readyAct.insert(_size,self.acts.get())
        else:
            for i in range(self.acts.qsize()):
                MyPipelineThread().readyAct.insert(0,self.acts.get())
        return self
    def excute(self):
        #调用解释器，解释动作。
        self._before_excute()
        MyPipelineThread().actionQueue.put(self)
        return self
    def _select(self,cssStr="",text="",memo="",ignoreErr=False,timeOut=3,errProcessCase='ignore'):
        if memo == "":
            memo = "正在选择选择器:..."
        self.acts.put({'way': 'select_option',
                       "cssStr": cssStr,'text':text,
                       'memo': memo, 'ignoreErr': ignoreErr,'timeOut':timeOut,
                       'errProcessCase': errProcessCase
                       })
        return self
    def _get_current_url(self,key="",memo="",ignoreErr=False,timeOut=3):
        """
                :param web: 访问的网站地址
                :return: 返回action丢向
                """
        if memo == "":
            memo = "正在获取当前网页网址:..."
        self.acts.put({'way': 'current_url',
                       "key": key,
                       'memo': memo, 'ignoreErr': ignoreErr,
                       'timeOut':timeOut
                       })
        return self

    # =============================================================================
    def jumpBrowserTab(self,index=-1,func=lambda x:x,func_args=[],pre_func=lambda x:True,pre_func_args=[]):
        self._args()
        return self
    def closeCurrentBroswserTab(self,func=lambda x:x,func_args=[],pre_func=lambda x:True,pre_func_args=[]):
        self._args()
        return self
    def get(self,url="",func=lambda x:x,func_args=[],pre_func=lambda x:True,pre_func_args=[]):
        """
        :param url: 访问的网站地址
        :return: 返回action丢向
        """
        self._args()
        return self
    def key_input(self,text="",cssStr="",isClear=True,func=lambda x:x,func_args=[],pre_func=lambda x:True,pre_func_args=[]):
        """
        在输入框输入内容。(小技巧:可以输入回车。让text=Keys.ENTER就可以)
        :param text:  {str} 输入框输入的内容，可以输入键值：如Keys.ENTER，则输入回车
        :param cssStr:  {str} 输入框的select选择器。
        :param isClear: {bol (True (default) | False)} 在输入输入框内容之前，是否先清空输入框。默认清空
        -当发生错误的时候的执行方案:
        """

        # if memo=="":
        #     memo="正在为"+cssStr+"输入框输入文字:"+str(text)
        # self.acts.put({'way': 'key_input',
        #                     "css": cssStr,
        #                     "text": text,
        #                     "isClear": isClear,
        #                     'memo':memo,
        #                })
        self._args()
        return self
    def click(self,cssStr="",index=0,func=lambda x:x,func_args=[],pre_func=lambda x:True,pre_func_args=[]):
        """
        根据css点击css的位置
        :param cssStr:  {str} 输入框的select选择器。
        当发生错误的时候的执行方案:
        ignore: 无视错误，继续执行。
        reStart_method: 重新开始本方法
        reStart_action: 重新开始整个动作链
        combine:综合方案
        """
        # print(self.buffer)
        # print(self.acts)
        self._args()
        # if memo=="":
        #     memo="正在点击按钮："+cssStr
        # self.acts.put({'way': 'click',
        #                "css": cssStr,
        #                "memo":memo,
        #                'index': index,
        #                     })  # 点
        return self
    def scroll_browser_top_to_button(self,func=lambda x:x,func_args=[],pre_func=lambda x:True,pre_func_args=[]):
        self._args()
        return self
    def sendDatas(self,key_datas="请为key赋值",datas='请为key_datas赋值',func=lambda x:x,func_args=[],pre_func=lambda x:True,pre_func_args=[]):
        self._args()
        return self
    def find(self,cssStr="",key="请为key赋值",mode="single" or "multiple",index=0,func=lambda x:x,catchDate=True,func_args=[],timeOut=3):
        """
        根据css点击css的位置
        :param cssStr: {str} 输入框的select选择器。
        :param key: {str} 爬取的信息的关键字。
        :param mode: {str("single"|"multiple")}
        single:爬取的模式爬取单个css选择器。multiple:爬取多个选择器，结果保存成数组
               """
        self._args()
        # if memo=="":
        #     memo="正在查找信息"+key+"其选择器为"+cssStr
        # self.acts.put({'way': 'find',
        #                    "css": cssStr,
        #                    "key": key,
        #                    "memo":memo,
        #                    'mode':mode,
        #                     'index':index
        #                })
        return self
    def initWeb(self, url="",func=lambda x:x,func_args=[],pre_func=lambda x:True,pre_func_args=[]):
        """
        初始化便签。将其他标签关闭。只留下一个标签那
        :return:
        """
        self._args()
        return self
if __name__ == '__main__':
    arr=[]
    arr.insert(0,1)
    arr.insert(0,2)
    arr.insert(0,3)
    print(arr)