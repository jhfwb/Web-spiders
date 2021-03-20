import sys
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    ElementNotInteractableException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
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
    def sendDatas(self,datas='请为key赋值',key_datas='请为key_datas赋值'):
        return self.pool.get().setState(success=True, actName=actName.sendDatas,datas=datas,key_datas=key_datas)
    def jumpBrowserTab(self,index=-1):#跳转到窗口
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return self.pool.get().setState(success=True, actName=actName.jumpBrowserTab,index=index)
    def closeCurrentBroswserTab(self):
        """
        当页面大于2个以上的时候，才会关闭
        此处注意：关闭掉该标签后，默认切换到最后一个标签卡
        :return:
        """
        if len(self.driver.window_handles)>=2:
            self.driver.close()
            self.driver.switch_to_window(self.driver.window_handles[-1])
        return self.pool.get().setState(success=True, actName=actName.closeCurrentBroswserTab)
    def select_option_apparent(self,cssStr,text,timeOut=3):
        if self._waitElement(cssStr,timeOut):
            s1 = Select(self._get_element_by_css_selector(cssStr=cssStr,timeOut=timeOut))
            s1.select_by_visible_text(text)
            return True
        else:
            return False
    #组合键等待
####################################################################################################################
    # 根据选择器，点击。点击完毕后，如果有添加新的页面，则会切换到新的页面
    def scroll_top_to_button(self,cssStr="",elemntName="",index=0,timeOut=5):
        interval_step = 30
        interval_time = 0.001
        wait_time=timeOut#等待时间
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
                    if cssStr!="" and elemntName!="":
                        if elemntName==self.driver.find_elements_by_css_selector(cssStr)[index].text.strip():
                            _sign=0
                            break
                    _index = _index+1
                    time.sleep(0.5)
                    go_height = self.driver.execute_script(js)
                    if _index>=_cycle_times:
                        _sign=0 #此处结束运行。
                        if cssStr=="" and elemntName=="":
                            break
                        elif cssStr!="":
                            return self.pool.get().setState(success=False, actName=actName.scroll_browser_top_to_button,errType=responseErr.elementNotFind,cssStr=cssStr)
                    continue
                else:#不等则继续运行
                    break
        return self.pool.get().setState(success=True, actName=actName.scroll_browser_top_to_button)
    def clickXY(self, x=0, y=0, left_click=True):
        '''
           dr:浏览器
           x:页面x坐标
           y:页面y坐标
           left_click:True为鼠标左键点击，否则为右键点击
        '''
        if left_click:
            ActionChains(self.driver).move_by_offset(x, y).click().perform()
        else:
            ActionChains(self.driver).move_by_offset(x, y).context_click().perform()
        ActionChains(self.driver).move_by_offset(-x, -y).perform()  # 将鼠标位置恢复到移动前
        return self.pool.get().setState(success=True, actName=actName.click,)
    def click_element_apparent(self,cssStr,loadNewPage=False,timeOut=3,index=0):
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
            element=self._get_elements_by_css_selector(cssStr=cssStr,timeOut=timeOut)[index]
            elementName=element.text.strip()
            try:
                if loadNewPage:
                    num=len(self.driver.window_handles)
                    element.click()
                    i=0
                    while True:
                        if len(self.driver.window_handles) - num == 1:
                            break
                        i = i + 1
                        if i == timeOut:
                            break
                        time.sleep(1)
                else:
                    element.click()
            except ElementClickInterceptedException: #该元素被遮挡,
                self.driver.execute_script('window.scrollTo(0, %s)' % (0))
                element.click()
            except ElementNotInteractableException:
                return self.pool.get().setState(success=False, actName=actName.click, cssStr=cssStr,errType=responseErr.elementClickFalse,index=index)
            return self.pool.get().setState(success=True, actName=actName.click, cssStr=cssStr,index=index,datas=elementName)
        else:

            return self.pool.get().setState(success=False, actName=actName.click, cssStr=cssStr,errType=responseErr.elementNotFind,index=index)
    def find_message_apparent(self, cssStr, key="", mode='single', timeOut=10,index=0):
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
                return self.pool.get().setState(success=True,actName=actName.findMessage,cssStr=cssStr,datas=item.text.strip(),key_datas=key,index=index)
            elif mode=='multiple':
                items=self._get_elements_by_css_selector(cssStr)
                arr=[]
                for item in items:
                    arr.append(item.text.strip())
                return self.pool.get().setState(success=True,actName=actName.findMessage,cssStr=cssStr,datas=arr,key_datas=key)
        else:
            return self.pool.get().setState(success=False,cssStr=cssStr,errType=responseErr.elementNotFind,actName=actName.findMessage)
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
    def inputwords_element_apparent(self, cssStr,text, isClear=True, timeOut=3):
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
                return self.pool.get().setState(success=True,actName=actName.inputWord,cssStr=cssStr)
             except Exception:
                return self.pool.get().setState(success=False,cssStr=cssStr,errType=responseErr.inputwordsErr,actName=actName.inputWord)
        else:
            return self.pool.get().setState(success=False,cssStr=cssStr,errType=responseErr.elementNotFind,actName=actName.inputWord)
    def initWeb(self,url=""):
        """
        初始化web
        :return: None
        """
        tagNum = len(self.driver.window_handles)
        for i in range(0, tagNum - 1):
            self._closeOtherTags()

        if url!="":
            return self.get_url(url=url).setState(actName=actName.initWeb)
        else:
            return self.pool.get().setState(success=True, actName=actName.initWeb)
    def get_current_url(self,key):
        current_url=None
        try:
            current_url=self.driver.current_url
        except TimeoutException:
            return self.pool.get().setState(success=False, actName=actName.findCurrentUrl,errType=responseErr.timeOutErr,key_datas=key)
        return self.pool.get().setState(success=True, actName=actName.findCurrentUrl,datas=current_url,key_datas=key)

    def _execute_js(self,line):
        return self.driver.execute_script(line)
    def get_url(self,url):
        """
        根据url访问网址
        :param url: 网址的名称
        :return:
        """
        try:
            self.driver.get(url)
            return self.pool.get().setState(success=True,actName=actName.askUrl)
        except Exception:
            return self.pool.get().setState(success=False,errType=responseErr.urlAskErr,actName=actName.askUrl)
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
    def suof(self):
        self.driver.execute_script("document.body.style.zoom='0.25'")
if __name__ == '__main__':
    # driver=ChormeDiver().driver
    # a=MyOption().get_url('https://www.baidu.com/')
    a=MyOption().moveXY()
    print("技术")


    # a=MyOption(driver).wait(cssStr='#hotsearch-content-wrapper > li:nth-child(3) > a > span.title-content-title>span',timeOut=0)
    # print(a)
    # MyOption.option(driver=driver,options={'way': 'init','memo':'memo','ignoreErr':'ignoreErr'})#初始化)