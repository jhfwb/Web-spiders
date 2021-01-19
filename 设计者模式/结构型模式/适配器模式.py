"""
适配器模式：
需求：现在有原始类Device(该类你不可改变)
现在，你需要通过适配器模式修改device中的一个方法。


"""

class Device(object):
    def click(self):
        print("普通点击")
    def delay(self):
        print("等待中")


class MyDevice(object):
    def sleep_click(self):
        print("等待1秒后再点击")

class Adapter(Device):#创建一个适配器，继承原对象
    def __init__(self):
        self.myDevice = MyDevice()
    def click(self):
        self.myDevice.sleep_click()

if __name__ == "__main__":
    target = Adapter()
    target.click()
    target.delay()
