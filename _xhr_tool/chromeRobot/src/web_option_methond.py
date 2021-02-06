import sys

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from pynput.keyboard import Listener
from pynput.keyboard import Key
import time
#操作工具
from _xhr_tool._annotate import singleObj
from _xhr_tool.chromeRobot.src._chromeRobot_tool.excuteResponsePool import ExcuteResponsePool
from _xhr_tool.chromeRobot.src._name.actName import actName
from _xhr_tool.chromeRobot.src._name.errName import responseErr
from _xhr_tool.chromeRobot.chromeConncet import ChormeDiver

timestamp_win = 0
@singleObj
class MyOption:
    itme={}
    username=""
    def __init__(self):
        self.driver=ChormeDiver().get_driver()
        self.pool=ExcuteResponsePool()
    #操作方法的汇总
    def option(self,options):
        """
        信息查找类。
        必须返回一个元组(key,value)
        """
        if options["way"]=="click":
            return self.click_element_apparent(cssStr=options['cssStr'],index=options['index'],option=options)
        elif options["way"]=="key_input": # 键入信息
            return self.inputwords_element_apparent(cssStr=options["cssStr"],text= options['text'],isClear=options['isClear'],option=options)
        elif options["way"]=="jumpBrowserTab":
            return self.jumpBrowserTab(index=options["index"],option=options)
        elif options["way"] == "closeCurrentBroswserTab":
            return self.closeCurrentBroswserTab(option=options)

        # elif options["way"] =="select_option":
        #     return MyOption.select_option_apparent(driver, options["css"], options['text'],options["timeOut"],options["errProcessCase"])
        # elif options["way"] =="wait":
        #     return MyOption.wait_util_key_press(driver)
        # elif options["way"] == "is_continue":
        #     pass
        elif options["way"]=="find":#查找信息
            return self.find_message_apparent(cssStr=options["cssStr"],key=options["key"],mode=options['mode'],index=options['index'],option=options)
        elif options["way"]=="get":
            return self.get_url(url=options["url"],option=options)
        elif options["way"]=="close":
            # return MyOption.closeTage(driver)
            pass
        elif options["way"] == "initWeb":
            return self.initWeb(url=options['url'],option=options)
        elif options["way"]=="screenshot":
            return MyOption._shot(driver,options["path"])
        elif options["way"]=="callback":
            return MyOption._callback(driver,options["method"])
        elif options["way"]=="current_url":
            return (options['key'],driver.current_url)
    @staticmethod
    def _callback(self,method):
        method()
        pass
    def _shot(self,path):
        """
        拍摄屏幕
        :param path: 文件保存的位置
        :return:
        """
        self.driver.save_screenshot(path)
    # 根据选择器，获得页面信息.text为key值
    @staticmethod
    def key_press(driver,text):
        pass
    @staticmethod
    def check_tag_status(driver,method,args):
        tagStatus = ["doNothing", "turnNewTag", "addNewTag", "removeOldTag"]  # 返回的标签状态。
        # 在点击之前先获取窗口句柄。
        windowsNum = len(driver.window_handles)
        oldCurrentHandle = driver.current_window_handle
        message=method(args)
        if message=='clear_action':
            return 'clear_action'
        if message=="actionFalse":
            return "actionFalse"
        windowsNumAfter = len(driver.window_handles)
        driver.switch_to.window(driver.window_handles[-1])  # 切换到最右边的标签卡
        # 判断标签状态
        tagState = windowsNumAfter - windowsNum
        if tagState == 0:
            # 判断是否有跳转新的页面
            if oldCurrentHandle == driver.current_window_handle:  # 没有跳转新页面
                return tagStatus[0]
            else:
                return tagStatus[1]
        elif tagState > 0:
            # 打开新标签
            return tagStatus[2]
        else:
            # 关闭了当前标签
            return tagStatus[3]
        pass
    def jumpBrowserTab(self,option,index=-1):#跳转到窗口
        self.driver.switch_to.window(self.driver.window_handles[index])
        return self.pool.getResponse().setState(success=True, actName=actName.jumpBrowserTab,index=index,option=option)
    def closeCurrentBroswserTab(self,option):
        self.driver.close()
        return  self.pool.getResponse().setState(success=True, actName=actName.closeCurrentBroswserTab,option=option)
    def select_option_apparent(self,cssStr,text,timeOut=3):
        if self._waitElement(cssStr,timeOut):
            s1 = Select(self._get_element_by_css_selector(cssStr=cssStr,timeOut=timeOut))
            s1.select_by_visible_text(text)
            return True
        else:
            return False
    #组合键等待
    @staticmethod
    def wait_util_key_press(driver):
        def on_press(key):
            global timestamp_win  # 这里先引入一个全局变量,用于储存时间戳.
            try:
                if key == Key.ctrl_l:  # 判断按键为Windows键
                    timestamp_win = time.time()  # 如果是就把当前的时间存进去
                if key == Key.enter:
                    # 判断另一个按键
                    if time.time() - timestamp_win < 0.5:  # 如果2次按键的时间小于0.5s,就执行你想要执行的函数,比如我想执行search函数.
                        listener.stop()
            except AttributeError:
                pass
        # def on_release(key):
        #     if key == keyboard.Key.esc:
        #         return False
        with Listener(on_press=on_press) as listener:
            listener.join()
####################################################################################################################
    # 根据选择器，点击。点击完毕后，如果有添加新的页面，则会切换到新的页面
    def click_element_apparent(self,cssStr,timeOut=3,index=0,option={}):
        """
        根据css选择器，点击元素。点击完毕后，如果有添加或者删除新的页面，则会将句柄切换到新的页面。
        每次执行完这个方法，必定会把句柄切换到最后一个-1
        :return: str 标签状态。
            标签状态：
            "doNothing",啥都没做
            "turnNewTag",关闭了原来的页面，并且打开了新的页面
            "addNewTag",打开了新的页面
            "removeOldTag"关闭了原来的页面
        """
        if  self._waitElement(cssStr,timeOut) == True:
            self._get_elements_by_css_selector(cssStr=cssStr,timeOut=timeOut)[index].click()
            return self.pool.getResponse().setState(success=True, actName=actName.click, cssStr=cssStr,index=index,option=option)
        else:
            return self.pool.getResponse().setState(success=False, actName=actName.click, cssStr=cssStr,errType=responseErr.elementNotFind,index=index,option=option)
    def find_message_apparent(self, cssStr, key="", mode='single', timeOut=10,index=0,option={}):
        """
        爬取网站信息
        :param cssStr:css选择器
        :param key:爬取信息的关键字。如要爬取电话：电话：13805980377 其中电话就是关键字。
        :param mode:single | multiple
                single：使用单个选择器。当有多个选择器的时候，选择第一个
                multiple： 使用多个选择器
        :return: e.g
        1.正常情况下：return (电话,13805980377）
        2.没有找到关键字(或者超时获取)：return actionFalse  中断操作
        3.没有找到关键字(或者超时获取)__忽略错误：return None   无视错误，继续下一步。
        """
        if  key ==None or key=="" :
            raise ValueError('key值不可为空字符串或者None。执行语句:'+str(sys._getframe(1).f_locals.get('options')))
        if  self._waitElement(cssStr,timeOut) == True:
            if mode=='single':
                item = self._get_elements_by_css_selector(cssStr)[index] # 此处存入方法
                return self.pool.getResponse().setState(success=True,actName=actName.findMessage,cssStr=cssStr,datas=item.text.strip(),key_datas=key,index=index,option=option)
            elif mode=='multiple':
                items=self._get_elements_by_css_selector(cssStr)
                arr=[]
                for item in items:
                    arr.append(item.text.strip())
                return self.pool.getResponse().setState(success=True,actName=actName.findMessage,cssStr=cssStr,datas=arr,key_datas=key,option=option)
        else:
            return self.pool.getResponse().setState(success=False,cssStr=cssStr,errType=responseErr.elementNotFind,actName=actName.findMessage,option=option)
    # 根据选择器，在文本框中键入text内容
    def _get_elements_by_css_selector(self, cssStr, timeOut=3):
        # type: (str,int)->[]
        """
        知道到css选择器，并返回数据。返回多个数据
        :param cssStr: 选择器的字符串
        :param timeOut: 超期时间
        :return:
        """
        elements= self.driver.find_elements_by_css_selector(cssStr)
        if len(elements)==0:
            return None
        return elements
    def _get_element_by_css_selector(self, cssStr, timeOut=3):
        # type: (str,int)->WebElement
        """
        知道到css选择器，并返回数据。返回多个数据
        :param cssStr: 选择器的字符串
        :param timeOut: 超期时间
        :return:
        """
        try:
            element=self.driver.find_element_by_css_selector(cssStr)
            return element
        except Exception:
            return None
    def inputwords_element_apparent(self, cssStr,text, isClear=True, timeOut=3,option={}):
        """
        在输入框中输入数字
        :param cssStr:
        :param text:
        :param isClear:
        :param timeOut:
        :return:
        """
        if self._waitElement(cssStr,timeOut):
            if isClear == True:
             try:
                self._get_element_by_css_selector(cssStr, timeOut).clear()
                self.driver.find_element_by_css_selector(cssStr).send_keys(text)
                return self.pool.getResponse().setState(success=True,actName=actName.inputWord,cssStr=cssStr,option=option)
             except Exception:
                return self.pool.getResponse().setState(success=False,cssStr=cssStr,errType=responseErr.inputwordsErr,actName=actName.inputWord,option=option)
        else:
            return self.pool.getResponse().setState(success=False,cssStr=cssStr,errType=responseErr.elementNotFind,actName=actName.inputWord,option=option)
    def initWeb(self,url="",option={}):
        """
        初始化web
        :return: None
        """
        tagNum = len(self.driver.window_handles)
        for i in range(0, tagNum - 1):
            self._closeOtherTags()

        if url!="":
            return self.get_url(url=url).setState(actName=actName.initWeb,option=option)
        else:
            return self.pool.getResponse().setState(success=True, actName=actName.initWeb,option=option)
    def scroll_top_to_button(self):
        interval_step = 30
        interval_time = 0.001
        wait_time=3 #等待时间
        interval_wait_time=0.5 #间隔甄别时间
        _cycle_times=wait_time/interval_wait_time #循环次数
        js = "return action=document.body.scrollHeight"
        go_height = self.driver.execute_script(js)
        current_height=0
        _sign=1
        while _sign==1:
            for i in range(current_height, go_height,interval_step):
                time.sleep(interval_time)
                self.driver.execute_script('window.scrollTo('+str(current_height)+', %s)' % (i))
            current_height=go_height
            go_height = self.driver.execute_script(js)
            _index = 0
            while True:
                if go_height == current_height:
                    _index=_index+1
                    time.sleep(0.5)
                    go_height = self.driver.execute_script(js)
                    if _index>=_cycle_times:
                        print('结束了')
                        _sign=0
                        break
                    continue
                else:
                    break
    def _execute_js(self,line):
        return self.driver.execute_script(line)
    def get_url(self,url,option={}):
        """
        根据url访问网址
        :param url: 网址的名称
        :return:
        """
        try:
            self.driver.get(url)
            return self.pool.getResponse().setState(success=True,actName=actName.askUrl,option=option)
        except Exception:
            return self.pool.getResponse().setState(success=False,errType=responseErr.urlAskErr,actName=actName.askUrl,option=option)
    def _waitElement(self,cssStr,timeOut=3):
        """
        内部方法。等待css选择器的出现，当出现的时候返回True,当超过timeOut
        后仍未出现，则返回False
        :param cssStr: css选择器
        :param timeOut: 等待时间，当超过等待时间，会抛出异常
        :return :
        """
        wait = WebDriverWait(self.driver, timeOut, 2)  #
        try:
            return wait.until(lambda driver: True if self.driver.execute_script(
                "return document.querySelector(\"" + cssStr + "\")") else False)
        except TimeoutException:
            return False
    def _closeOtherTags(self):
        # type: ()->None
        """
        驱动谷歌浏览器，使得关闭其他标签，只留第一个标签
        """
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])

if __name__ == '__main__':
    driver=ChormeDiver().driver
    # a=MyOption().get_url('https://www.baidu.com/')
    a=MyOption().scroll_top_to_button()


    # a=MyOption(driver).wait(cssStr='#hotsearch-content-wrapper > li:nth-child(3) > a > span.title-content-title>span',timeOut=0)
    # print(a)
    # MyOption.option(driver=driver,options={'way': 'init','memo':'memo','ignoreErr':'ignoreErr'})#初始化)