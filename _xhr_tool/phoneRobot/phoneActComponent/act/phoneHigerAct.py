import os
from uiautomator2 import Device
from _xhr_tool._utils.RUtils import tool
from _xhr_tool.phoneRobot.phoneActComponent.act.phoneBaseAct import PhoneBaseAct

class PhoneHigherAct:
    """
    操作手机的机器人，该类理应封装操作方法。底层操作。建议
    """
    def __init__(self,device:Device):
        self._baseAct=PhoneBaseAct(device)
        self._device = device # 获得老设备
        # self.device = self._packDevice(device)  # 新封装的设备
    def _packDevice(self,device):
        """
        由于无法解决循环引用的问题，因此将引用调入到方法中执行。该方法的目的只有一个，就是让编译器能够识别，使得
        在书写新方法的时候更加便捷
         """
        from _xhr_tool.phoneRobot import Device
        return Device(device)
    def sendMessages(self,isSend=False,phonesAndMessages=[]):
        for phonesAndMessage in phonesAndMessages:
            pass

        pass
    def sendMessage(self,phone='',message='',isSend=False):
        # type:(str,str,bool) -> tuple
        """

        负责编辑短信，并发送短信。定制软件
        eg:
        :param phone: 发送短信的手机号
        :param message: 发送的短信的内容
        :param isSend:  是否发送短信。
        :return: tuple 返回(电话,内容)
        """
        #判断phone与message是否合法。
        phone=str(phone)
        message=str(message)
        self._baseAct.press('home', note="点击home键")
        self._baseAct.startApp('com.android.mms', note="点击home键")
        self._baseAct.click(0.86, 0.936,note="信息图标-添加短信")
        self._baseAct.send_keys(phone,x=0.409,y=0.151,note="信息图标-添加短信-收件人选框-输入电话号码")
        self._baseAct.send_keys(message, 0.364,y=0.907,note="信息图标-添加短信-输入短信内容")
        if isSend==True:
            self._baseAct.click(x=0.909, y=0.915, note='发送信息', sleeptime=0.5)
        self._baseAct.press('back',note="返回")
        self._baseAct.click(0.036, 0.071, note="信息图标-添加短信-返回")
        return (phone,message)
    @staticmethod
    def _openPrint(note):
        """
        控制台打印信息，内部方法
        """
        tool.print(note,fontColor='red')
    @staticmethod
    def debug():
        """
        打开手机的调试模式的服务器。
        """
        os.system('python -m weditor')
if __name__ == '__main__':
    print('——————————开始测试——————————')
    device=PhoneConnectAssistant().usbConncet()
    device.send_keys("00000")
    # PhoneAct.startApp(device,'com.android.gallery3d')# 打开app程序，打开图库
    #
    # PhoneAct.click(device,100,100)
