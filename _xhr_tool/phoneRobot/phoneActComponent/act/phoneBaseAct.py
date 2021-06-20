import os
import time
from uiautomator2 import Device
from uiautomator2.exceptions import XPathElementNotFoundError

from _xhr_tool._utils.RUtils import tool
from _xhr_tool.phoneRobot.phoneActComponent.logger import log


class PhoneBaseAct:#本身也属于设备
    """
    操作手机的机器人，该类理应封装操作方法。底层操作。
    1.点击
    2.滑屏
    3.延迟
    4.根据包名开始程序。
    5.
    """
    def __init__(self,device:Device):
        self._device=device# 获得老设备
        # self.device=self._packDevice(device)#新封装的设备
    def _packDevice(self,device):
        """
        由于无法解决循环引用的问题，因此将引用调入到方法中执行。该方法的目的只有一个，就是让编译器能够识别，使得
        在书写新方法的时候更加便捷
        """
        from _xhr_tool.phoneRobot import Device
        return Device(device=device)


    @log
    def startApp(self,name="",stop=False):
        """
        根据手机软件的包名，打开程序。
        :parma device 执行该操作的手机对象。通常是由usbConnect产生。
        :parma name 其中name为app的名称，如果不知道app对应的name，可以通过调试debug()方法获取app软件的名称
        具体方法是这样的：连接好weditor后，然后点击进入一个软件，软件中一个package。里面的值就是name的值
        """
        tool().print("正在打开软件"+str(self._device.app_current()),fontColor='blue')
        self._device.app_start(name, stop=False)

    @log
    def screen_off(self):
        """
        关闭设备屏幕
        """
        return  self._device.screen_off()

    @log
    def screen_on(self):
        """
        打开设备屏幕
        """
        return self._device.screen_on()

    @log
    def delay(self,secound=0):
        """
        延迟时间
        """
        time.sleep(secound)

    @log
    def click(self,x,y,sleeptime=0.1):
        """
        根据x与y的位置，点击手机上的坐标点。
        """
        self._device.click(x,y)
        self.delay(sleeptime)

    @log
    def click_byName(self, name="",sleeptime=0.1):
        """
        根据名称点击对应元素
        :parma device 执行该操作的手机对象。通常是由usbConnect产生。
        :parma name 其中name为app的名称，如果不知道app对应的name，可以通过调试debug()方法获取app软件的名称
        具体方法是这样的：连接好weditor后，然后点击进入一个软件，软件中一个package。里面的值就是name的值
        """
        print('开始运行')
        a=self._device.xpath('//*[@text="'+name+'"]')
        # self.delay(sleeptime)
        if a.exists==False:
            return False
        else:
            try:
                a.click()
                return True
            except XPathElementNotFoundError:
                return False
    @log
    def press(self,key,sleeptime=0.1):
        self._device.press(key)
        self.delay(sleeptime)

    @log
    def send_keys(self,message,x=-1,y=-1,sleeptime=0.1,isClear=False):
        """
        在手机文本框中输入参数message的内容。
        :param message 文本框输入的内容
        :param x 文本框的位置x，对于已经在焦点的文本框，可以不设置该参数
        :param y 文本框的位置y，对于已经在焦点的文本框，可以不设置该参数
        :param sleeptime 停顿时间
        :param isClear 是否将文本框的原有内容清除，默认不清除
        """
        if x!=-1 and y!=-1:
            self._device.click(x, y)
            self.delay(sleeptime)
        if isClear==True:
            self._device.clear_text()
        time.sleep(sleeptime)
        self._device.send_keys(message)
        time.sleep(sleeptime)
    @staticmethod
    def debug():
        """
        打开手机的调试模式的服务器。一般不会使用
        """
        os.system('python -m weditor')