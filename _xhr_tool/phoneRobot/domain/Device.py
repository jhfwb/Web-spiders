from uiautomator2 import Device as device1
from _xhr_tool.phoneRobot.connectComponent.ConnectMenager import PhoneConnectAssistant
# from _xhr_tool.phoneRobot.phoneActComponent import PhoneBaseAct, PhoneHigherAct
from _xhr_tool.phoneRobot.phoneActComponent.act.phoneBaseAct import PhoneBaseAct
from _xhr_tool.phoneRobot.phoneActComponent.act.phoneHigerAct import PhoneHigherAct


class Device:
    """
    设备类。主要功能为提供一
    """
    act="动作域"
    _device="原封装的设备对象"
    def __init__(self,device=""):
        if device!="":
            self._device = device
        else:
            #获得旧的设备
           self._device=PhoneConnectAssistant().usbConncet()
        # 2.初始化基础动作
        self.act = _phoneAct(base=PhoneBaseAct(self._device), higher=PhoneHigherAct(self._device))
    def getOldDevice(self) -> device1:
        #获得老设备
        return self._device
class _phoneAct:#动作域
    base = "基础动作对象"
    higher="高级动作对象"
    def __init__(self,base:PhoneBaseAct,higher:PhoneHigherAct):
        self.base=base
        self.higher=higher
if __name__ == '__main__':
    # Device().act.
    # device.act.base.startApp('com.android.gallery3d')
    tu=Device().act.higher.sendMessage(phone='13805980379',message='你好')

    # 写一个方法。将字符串写入到指定文本中。
    print(tu)
