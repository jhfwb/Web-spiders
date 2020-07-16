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
    def get_current_url(self,key="",memo="",ignoreErr=False,timeOut=3):
        """
                @param web: 访问的网站地址
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
    def get(self,web="",memo="",ignoreErr=False):
        """

        @param web: 访问的网站地址
        :return: 返回action丢向
        """
        if memo=="":
            memo="正在访问网址:"+web+"..."
        self.acts.put({'way': 'get',
                            "text": web,'memo':memo,'ignoreErr':ignoreErr
                            })
        return self

    def key_input(self,text="",cssStr="",isClear=True,memo="",ignoreErr=False,timeOut=3,errProcessCase="ignore"):
        """
        在输入框输入内容。(小技巧:可以输入回车。让text=Keys.ENTER就可以)


        @param text:  {str} 输入框输入的内容，可以输入键值：如Keys.ENTER，则输入回车

        @param cssStr:  {str} 输入框的select选择器。

        @param isClear: {bol (True (default) | False)} 在输入输入框内容之前，是否先清空输入框。默认清空

        @param ignoreErr: 是否无视错误。目前是废参数

        @param errProcessCase: {str ('ignore' | 'reStart_method' | 'reStart_action') }
        -当发生错误的时候的执行方案:
        ignore: 无视错误，继续执行。
        reStart_method: 重新开始本方法
        reStart_action: 重新开始整个动作链

        """
        if memo=="":
            memo="正在为"+cssStr+"输入框输入文字:"+str(text)
        self.acts.put({'way': 'key_input',
                            "css": cssStr,
                            "text": text,
                            "isClear": isClear,'memo':memo,'ignoreErr':ignoreErr,
                             'timeOut':timeOut,
                            'errProcessCase':errProcessCase
                       })
        return self
    def click(self,cssStr="",memo="",ignoreErr=False,success=lambda x:x,exception=lambda x:x,timeOut=3,errProcessCase="ignore"):
        """
        根据css点击css的位置

        @param cssStr:  {str} 输入框的select选择器。

        @param memo: {str} 备注，说明

        @param ignoreErr {bol}  是否无视错误。目前是废参数

        @param success {function} 这是一个方法,当方法执行成功会执行这个方法。该有只有一个参数，参数尾action对象。

        @param exception {function} 这是一个方法,当方法执行失败会执行这个方法。该有只有一个参数，参数尾action对象。

         @param timeOut: {int} 默认3秒。当超过3秒后，该方法如果还没能成功执行，则默认失败

         @param errProcessCase: {str ('ignore' | 'reStart_method' | 'reStart_action'|'combine') }
        当发生错误的时候的执行方案:
        ignore: 无视错误，继续执行。
        reStart_method: 重新开始本方法
        reStart_action: 重新开始整个动作链
        combine:综合方案
        """
        if memo=="":
            memo="正在点击按钮："+cssStr
        self.acts.put({'way': 'click',
                       "css": cssStr,
                       "memo":memo,
                       'ignoreErr':ignoreErr,
                       'success':success,
                       'exception':exception,
                       'action':self,
                       'timeOut': timeOut,
                       'errProcessCase': errProcessCase
                            })  # 点
        return self
    def find(self,cssStr="",key="",memo="",ignoreErr=False,mode="",timeOut=3,errProcessCase="ignore"):
        """
       根据css点击css的位置

       @param cssStr {str} 输入框的select选择器。

       @param key {str} 爬取的信息的关键字。

       @param memo: {str} 备注，说明

       @param ignoreErr {bol}  是否无视错误。目前是废参数

       @param mode {str("single"|"multiple")}
       single:爬取的模式爬取单个css选择器。multiple:爬取多个选择器，结果保存成数组

        @param timeOut {int} 默认3秒。当超过3秒后，该方法如果还没能成功执行，则默认失败

        @param errProcessCase: {str ('ignore' | 'reStart_method' | 'reStart_action'|'combine') }
       -当发生错误的时候的执行方案:
       ignore: 无视错误，继续执行。
       reStart_method: 重新开始本方法
       reStart_action: 重新开始整个动作链
       combine:综合方案
               """
        if memo=="":
            memo="正在查找信息"+key+"其选择器为"+cssStr
        self.acts.put({'way': 'find',
                           "css": cssStr,
                           "key": key,
                           "memo":memo,
                           'ignoreErr':ignoreErr,
                            'mode':mode,
                       'timeOut': timeOut,
                       'errProcessCase': errProcessCase
                       })
        return self


