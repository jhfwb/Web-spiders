from abc import ABCMeta
from abc import abstractmethod


class Payclass(metaclass=ABCMeta):
    @abstractmethod
    def pay(self):
        pass

    @abstractmethod
    def haha(self):
        print('haha')
class Ali(Payclass):
    def pay(self, money):
        print("使用阿里支付{money}".format(money=money))
# 如果想使用抽象类，则只需要继承这个抽象类就可以了
class Ten(Payclass):
    def pay(self, money):
        print("使用微信支付{money}".format(money=money))
class App(Payclass):
    def pay(self, money):
        print("使用苹果支付{money}".format(money=money))
if __name__ == '__main__':
    Ali().haha()
