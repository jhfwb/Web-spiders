#专门用来读取配置信息的
import configparser


class MyConfig:
    def __init__(self):
        #读取配置信息
        cf = configparser.ConfigParser()
        self.cf=cf
        cf.read("setting.ini", encoding="utf-8")  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块
        self.功能 = cf.get("4life", "功能")
        self.收货人=cf.get("add_address", "收货人")
        self.邀请人=cf.get("register","邀请人")
        self.邀请码=cf.get("yao",self.邀请人)
    def read_data(self):#此方法比较耗时间，需要请调用
        self.cf.read("data.ini", encoding="utf-8")
        account=self.cf.items("account")
        self.所有账户与密码=account

