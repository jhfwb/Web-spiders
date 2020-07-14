from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from pynput.keyboard import Listener
from pynput.keyboard import Key
import time
#操作工具
timestamp_win = 0
class MyOption:
    itme={}
    username=""
    #操作方法的汇总
    @staticmethod
    def option(driver,options):
        """
        信息查找类。
        必须返回一个元组(key,value)
        """
        if options["way"]=="click":#点击
            return MyOption.check_tag_status(driver=driver,method=MyOption.click_element_apparent,args={'driver':driver,'cssStr':options["css"],'ignoreErr':options["ignoreErr"]})
        elif options["way"]=="key_input":#键入信息
            return MyOption.input_words_element_apparent(driver, options["css"], options['text'],options['isClear'])
        elif options["way"] =="select_option":#选择select
            return MyOption.select_option_apparent(driver, options["css"], options['text'])
        elif options["way"] =="wait":#选择select
            return MyOption.wait_util_key_press(driver)
        elif options["way"] == "is_continue":  # 选择select
            return MyOption.is_continue(driver)
        elif options["way"]=="find":
            return MyOption._find_message_apparent(driver,options["css"],options["key"],options["ignoreErr"],mode=options['mode'])
        elif options["way"]=="get":
            return MyOption._get_url(driver,options["text"])
        elif options["way"]=="close":
            return MyOption.closeTage(driver)
        elif options["way"] == "init":
            return MyOption.initWeb(driver)
        elif options["way"]=="screenshot":
            return MyOption._shot(driver,options["path"])
        elif options["way"]=="callback":
            return MyOption._callback(driver,options["method"])
        elif options["way"]=="current_url":
            return (options['key'],driver.current_url)

    @staticmethod
    def _callback(driver,method):

        method()
        pass

    @staticmethod
    def _shot(driver,path):
        """
        拍摄屏幕
        :param driver: 谷歌驱动
        :param path: 文件保存的位置
        :return:
        """
        driver.save_screenshot(path)
    @staticmethod
    def initWeb(driver):
        """
        初始化谷歌浏览器。（关闭其他浏览器标签，只保留一个浏览器标签）
        :param driver:谷歌驱动
        :return:
        """
        tagNum=len(driver.window_handles)
        for i in range(0,tagNum-1):
            MyOption._closeOtherTags(driver)
    @staticmethod
    def _closeOtherTags(driver):
        """
        驱动谷歌浏览器，使得关闭其他标签，只波流第一个标签
        :param driver:
        :return:
        """
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
    #发出请求
    @staticmethod
    def _get_url(driver,url):
        """
        根据url访问网址
        :param driver:
        :param url: 网址
        :return:
        """
        driver.get(url)
    # 根据选择器，获得页面信息.text为key值
    @staticmethod
    def _find_message_apparent(driver, cssStr,key,ignoreErr,mode='single'):
        """
        爬取网站信息
        :param driver:谷歌驱动
        :param cssStr:css选择器
        :param key:爬取信息的关键字。如要爬取电话：电话：13805980377 其中电话就是关键字。
        :param ignoreErr:True | False  是否无视错误。出现错误的话，是否中断整个行动链。
        :param mode:single | multiple
                single：使用单个选择器。当有多个选择器的时候，选择第一个
                multiple： 使用多个选择器
        :return: e.g
        1.正常情况下：return (电话,13805980377）
        2.没有找到关键字(或者超时获取)：return actionFalse  中断操作
        3.没有找到关键字(或者超时获取)__忽略错误：return None   无视错误，继续下一步。
        """
        command=MyOption.my_wait(driver, cssStr)
        if command==True:
            item=MyOption.my_find_element_by_css_selector(driver, cssStr,mode)#此处存入方法
            if type(item)==type([]):
                arr=[]
                for ite in item:
                    arr.append(ite.text.strip())
                return (key, arr)
            elif type(item.text)==type(""):
                return (key, item.text.strip())
            else:
                pass
        elif command=="actionFalse":
            if ignoreErr == True:
                return None
            return "actionFalse"


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

    #根据选择器，点击。点击完毕后，如果有添加新的页面，则会切换到新的页面
    @staticmethod
    def click_element_apparent(options):
        """
        根据css选择器，点击元素。点击完毕后，如果有添加或者删除新的页面，则会将句柄切换到新的页面。
        每次执行完这个方法，必定会把句柄切换到最后一个-1
        :param driver: 浏览器驱动
        :param cssStr: 字符串类型。css选择器
        :return: str 标签状态。
            标签状态：
            "doNothing",啥都没做
            "turnNewTag",关闭了原来的页面，并且打开了新的页面
            "addNewTag",打开了新的页面
            "removeOldTag"关闭了原来的页面

        """
        command=MyOption.my_wait(options['driver'],options['cssStr'])
        if command==True:
            MyOption.my_find_element_by_css_selector(options['driver'], options['cssStr']).click()
        elif command=="actionFalse":
            if options['ignoreErr']==True:
                return None
            return "actionFalse"

    #根据选择器，在文本框中键入text内容
    @staticmethod
    def input_words_element_apparent(driver,cssStr,text,isClear=True):
        command =MyOption.my_wait(driver,cssStr)
        if command==True:
            if isClear==True:
                MyOption.my_find_element_by_css_selector(driver,cssStr).clear()
            driver.find_element_by_css_selector(cssStr).send_keys(text)
        elif command=="actionFalse":
            return "actionFalse"
    #根据选择器，在select选框中，选择可视文本option属性
    @staticmethod
    def my_wait(driver, cssStr):
        """
        未找寻到css。则会返回false。
        :param driver:
        :param cssStr:
        :return:
        """
        wait = WebDriverWait(driver,5, 2)
        try:
            wait.until(lambda driver: True if driver.execute_script("return document.querySelector(\"" + cssStr + "\")") else False)
            return True
        except TimeoutException:
            return "actionFalse"

    @staticmethod
    def my_find_element_by_css_selector(driver,cssStr,mode='single'):
        if MyOption.my_wait(driver, cssStr):
            if mode=='single':
                return driver.find_element_by_css_selector(cssStr)
            elif mode=='multiple':
                return driver.find_elements_by_css_selector(cssStr)
            else:
                return driver.find_element_by_css_selector(cssStr)
    @staticmethod
    def select_option_apparent(driver,cssStr,text):
        MyOption.my_wait(driver,cssStr)
        s1 = Select(MyOption.my_find_element_by_css_selector(driver, cssStr))
        s1.select_by_visible_text(text)
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

    # #在前端执行js代码，判断是否可用，如果可用就放行，如果不可用就发起等待
    # @staticmethod
    # def is_continue(driver):
    #     while True:
    #         wait = WebDriverWait(driver, 200, 2)  # 显示等待
    #         wait.until(lambda driver: True if driver.execute_script("return confirm('是否继续?')") else False)
    #         if driver.execute_script("return confirm('是否继续?')")==False|None:
    #             MyOption.wait_util_key_press(driver)
    #         else:
    #             break