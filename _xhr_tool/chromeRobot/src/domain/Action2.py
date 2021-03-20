import inspect
import sys
import uuid
#ignoreErr 是否无视错误。如果动作出错，则中断后续操作。如果无视了，则继续执行下面的操作
from _utils.RUtils import tool

from _xhr_tool.chromeRobot.src.domain.ChromeFactory import ChromeFactory
from _xhr_tool.chromeRobot.src.web_option_methond2 import MyOption
from _xhr_tool.excuteEngine.Engine import ExcuteFuel


class Action:
    """
    为每个动作添加一个uid
    注意事项！此处的方法命名必须与web_opeion_methond中的方法一致
    行动。
    # 1. 将方法中的参数变成一个对象。
    # 2. 将对象只行推站处理
    """
    def __init__(self):
        self.chromeFactory=ChromeFactory()
        self.excuteEngine=self.chromeFactory.engine
        self._bufferActs=[]
        self._uid=str(uuid.uuid1())
    def findCurrentUrl(self,key="current_url",catchDate=True,ignoreErr=False,func=lambda x:x,func_args=[],pre_func=lambda x:True,pre_func_args=[]):
        """
        获得当前页面的url
        :return:
        """
        func = MyOption().get_current_url
        self._args()
        return self
    def connectLastBackFunction(self,after_func=lambda x:x,after_func_args=[]):
        """
        连接到上一个方法的回调函数的返回值。该返回值会作为参数传入并传入次此方法。(比较难理解)
        #复合型方法，可能没法使用哦
        :param func:
        :return:
        """
        def func():
            fuel: ExcuteFuel = self.excuteEngine.getHistoryExcuteList()[0]
            return fuel.get_func_result()
        self._args()
        return self
    def excuteBlock(self,isSave=False):
        if isSave:
            self._bufferActs.append(self.excuteEngine.getNewFuel().setFuel(meta={'act': 'save', 'id': self._uid}))
        self.excuteEngine.put_excuteFuelCache(fuels=self._bufferActs)  # 将其
        self.excuteEngine.excuteFuelCache()
        self.excuteEngine.block()
    def excute(self,isSave=False):
        """

        :param isSave:
        :return:
        """
        #调用解释器，解释动作。
        if isSave:
            self._bufferActs.append(self.excuteEngine.getNewFuel().setFuel(meta={'act':'save','id':self._uid}))
        self.excuteEngine.put_excuteFuelCache(fuels=self._bufferActs) # 将其
        self.excuteEngine.excuteFuelCache()
        return self
    def excuteRightNow(self,isSave=False):
        if isSave:
            self._bufferActs.append(self.excuteEngine.getNewFuel().setFuel(meta={'act':'save', 'id': self._uid}))
        self.excuteEngine.put_excuteFuelCache(fuels=self._bufferActs) # 将其
        self.excuteEngine.excuteFuelCache(excuteOrder='first')
        return self
    # =============================================================================
    def _args(self):#对参数进行处理的中间方法
        """
        1.获取方法中的固定参数'after_func_args' or 'after_func'or 'after_func_kwargs' or 'before_func' or 'before_func_args' or key=='before_func_kwargs' :
        2.
        :return:
        """
        # methodName=sys._getframe(1).f_code.co_name #获得方法名称
        valueDict=sys._getframe(1).f_locals #获得方法名称
        valueDict.pop('self')
        dict_args={}
        dict_func={}
        dict_meta={}
        dict_meta.setdefault('id', self._uid)
        args_arr=[]
        if valueDict.get('func')!=None:
            args_arr = inspect.getfullargspec(valueDict.get('func')).args
        for key, values in valueDict.items():
            if key=='func'or key=='after_func_args' or  key=='after_func'or key=='after_func_kwargs' or  key=='before_func' or  key=='before_func_args' or key=='before_func_kwargs' :
                dict_func.setdefault(key,values)
            elif key in args_arr:
                dict_args.setdefault(key,values)
            else:

                dict_meta.setdefault(key,values)
        self._bufferActs.append(self.excuteEngine.getNewFuel().setFuel(
            func=dict_func.get('func'), func_kwargs=dict_args,
            before_func=dict_func.get('before_func'),before_func_args=dict_func.get('before_func_args'),
            after_func=dict_func.get('after_func'),after_func_args=dict_func.get('after_func_args'),meta=dict_meta)
        )
    def clickXY(self,x=0,y=0):

        func = MyOption().clickXY
        self._args()
        return self
    def jumpBrowserTab(self,index=-1,ignoreErr=False,after_func=lambda x:x,after_func_args=[],before_func=lambda:True,before_func_args=[]):
        func=MyOption().jumpBrowserTab
        self._args()
        return self
    def closeCurrentBroswserTab(self,ignoreErr=False,after_func=lambda x:x,after_func_args=[],before_func=lambda:True,before_func_args=[]):
        func = MyOption().closeCurrentBroswserTab
        self._args()
        return self
    def get(self,url="",ignoreErr=False,after_func=lambda x:x,after_func_args=[],before_func=lambda:True,before_func_args=[]):
        """
        :param url: 访问的网站地址
        :return: 返回action丢向
        """
        func = MyOption().get_url
        self._args()
        return self
    def key_input(self,text="",cssStr="",isClear=True,ignoreErr=False,after_func=lambda x:x,after_func_args=[],before_func=lambda:True,before_func_args=[]):
        """
        在输入框输入内容。(小技巧:可以输入回车。让text=Keys.ENTER就可以)
        :param text:  {str} 输入框输入的内容，可以输入键值：如Keys.ENTER，则输入回车
        :param cssStr:  {str} 输入框的select选择器。
        :param isClear: {bol (True (default) | False)} 在输入输入框内容之前，是否先清空输入框。默认清空
        -当发生错误的时候的执行方案:
        """
        func = MyOption().inputwords_element_apparent
        self._args()
        return self
    def click(self,cssStr="",index=0,loadNewPage=False,ignoreErr=False,after_func=lambda x:x,after_func_args=[],before_func=lambda:True,before_func_args=[]):
        """
        根据css点击css的位置
        :param cssStr:  {str} 输入框的select选择器。
        当发生错误的时候的执行方案:
        ignore: 无视错误，继续执行。
        reStart_method: 重新开始本方法
        reStart_action: 重新开始整个动作链
        combine:综合方案
        """
        func = MyOption().click_element_apparent
        self._args()
        return self
    def scroll_browser_top_to_button(self,ignoreErr=True,cssStr="",index=0,timeOut=5,elemntName="",after_func=lambda x:x,after_func_args=[],before_func=lambda:True,before_func_args=[]):
        func = MyOption().scroll_top_to_button
        self._args()
        return self
    def find(self,ignoreErr=True,cssStr="",key="请为key赋值",mode="single" or "multiple",index=0,timeOut=3,catchDate=False,after_func=lambda x:x,after_func_args=[],before_func=lambda:True,before_func_args=[]):
        """
        根据css点击css的位置
        :param cssStr: {str} 输入框的select选择器。
        :param key: {str} 爬取的信息的关键字。
        :param mode: {str("single"|"multiple")}
        single:爬取的模式爬取单个css选择器。multiple:爬取多个选择器，结果保存成数组
               """
        func = MyOption().find_message_apparent
        self._args()
        return self
    def sendDatas(self,ignoreErr=False,key_datas="请为key赋值",datas='请为key_datas赋值',catchDate=False,after_func=lambda x:x,after_func_args=[],before_func=lambda:True,before_func_args=[]):
        func = MyOption().sendDatas
        self._args()
        return self
    def initWeb(self, url="",ignoreErr=False,after_func=lambda x:x,after_func_args=[],before_func=lambda:True,before_func_args=[]):
        """
        初始化便签。将其他标签关闭。只留下一个标签那
        :return:
        """
        func = MyOption().initWeb
        self._args()
        return self
if __name__ == '__main__':
    import time

    # def test(resutl):
    #     print(resutl)
    #     Action().key_input(cssStr='#kw',text='你好').excuteRightNow()
    # Action().initWeb(url='https://www.baidu.com/').find(cssStr='#kw',after_func=test).click(cssStr='.title-content-title').excute()