import os
import uiautomator2 as u2
class PhoneConnectAssistant:
    """
    手机连接助手

    用于负责连接手机的助手。
    1.usb方式连接手机。
        当手机首次连接的时候将通知下载对应app
    2.ip方式连接手机
    """
    def __init__(self):
        self.device=''
        pass
    def usbConncet(self):
        #python -m uiautomator2 init  在手机上安装客户端。
        """
        使用usb方式连接手机。如果该手机没有下载atx，将会指导其下载atx。
        """
        # try:
        os.system('python -m uiautomator2 init') #在手机上初始化客户端，如果没有该客户端则下载。
        self.device = u2.connect()
        print('成功连接手机!')
        # except RuntimeError:
        #     print('没有找到任何使用usb连接的设备！请确保该手机已经允许usb调试！')
        # return self.device
        return self.getDecive()
    def walnConncet(self,ip):
        """
        使用wifi的ip无线连接手机。如何获取手机的ip。首先，确保手机和电脑在同一个wifi下面。然后在手机上打开atx软件，
        当然，如果没有这个软件，那只能使用usb连接。
        """
        d = u2.connect(ip)
        return d
    # def snConnect(self):
    #     d=u2.connect('5ENDU19A29003986')
    #     return d

    def getDecive(self):
        return self.device
if __name__ == '__main__':
    assistant=PhoneConnectAssistant()
    assistant.usbConncet()

