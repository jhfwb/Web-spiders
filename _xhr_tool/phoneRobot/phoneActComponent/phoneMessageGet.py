class PhoneMessageGet:
    """
    负责获取手机的基本操作信息。
    1.获取手机当前程序的包名。
    ...
    """

    @staticmethod
    def getPackageName(device):
        """
        获取当前包的名称。
        :parma device 执行该操作的手机对象。通常是由usbConnect产生。
        """
        return device.current_app().package
    @staticmethod
    def isScreenOn(device):
        """
        判断屏幕状态。是否是打开的状态，true or false
        """
        return device.info.get('screenOn')
    @staticmethod
    def getSn(device):
        """
        获取当前包的名称。
        :parma device 执行该操作的手机对象。通常是由usbConnect产生。
        """
        return device.serial
    @staticmethod
    def getWlanIp(device):
        """
        获得当前该手机连接wifi的ip地址
        """
        return device.wlan_ip

    @staticmethod
    def getIp(device):
        """
        获取当前包的名称。
        :parma device 执行该操作的手机对象。通常是由usbConnect产生。
        """
        return device.wlan_ip

if __name__ == '__main__':
    # r=PhoneAct.debug()
    print('——————————开始测试——————————')
    # device = PhoneConnectAssistant().walnConncet(test_IP)
    device = PhoneConnectAssistant().usbConncet()

    print(PhoneMessageGet().isScreenOn(device))