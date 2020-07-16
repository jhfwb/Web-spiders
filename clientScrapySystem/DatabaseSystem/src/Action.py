#coding:utf-8
import re
import time
from clientScrapySystem.DatabaseSystem.src.CsvToXlsx import CsvToXlsx
from clientScrapySystem.DatabaseSystem.template.keyArr import KEY_ARR
from clientScrapySystem.DatabaseSystem.utils.DatabaseHandler import DatabaseHandler
from clientScrapySystem.DatabaseSystem.utils.Engine import Engine, Task
from clientScrapySystem.chromeRobotSystem.Context import Context
from clientScrapySystem.chromeRobotSystem.天眼查 import 天眼查
from utils.RR_Comments import PrintTool
class Action:
    def main(self):
        self.con=Context()
        self.con.main()
        self.hander=DatabaseHandler()
        self.天眼查=天眼查()
        def first_():# 监听smelter中有没有数据。将smelter中的csv文件转成xlsx文件。并转存到0_初始客户群的数据库中
            PrintTool.print('first_方法开始执行!',fontColor='gray')
            bol=CsvToXlsx().working()
            datas=self.hander.transfer(FromDatabseName='smelter',ToDatabaseName='0_初始客户群',num=-1)
            #启动机器人吧。可以开始验证了
        def secound_():#将数据从0中取出来，并
            PrintTool.print('secound_方法开始执行!', fontColor='gray')
            def use天眼查Robot(data):#经过天眼查处理，获得的天眼查数据
                self.天眼查.run(self.con.robotThread, data['公司名'])
                items=self.con.robotThread.itemsQueue.get()#爬取的信息
                if type(items['手机'])==type([]):
                    line=""
                    for phone in items['手机']:
                        line+=phone+"|||"
                    items['手机']=line[0:len(line)-3]
                return items
            def filterFunction_site(data):
                citys = KEY_ARR.getSiteArr()
                for city in citys:
                    if data['公司名']!=None:
                        if city in data['公司名']:
                            return True
                    if data['地址'] != None:
                        if city in data['地址']:
                            return True
                    if data['城市'] != None:
                        if city in data['城市']:
                            return True
                    if data['信息'] != None:
                        if city in data['信息']:
                            return True
                    if data['产品'] != None:
                        if city in data['产品']:
                            return True
                return False
            def filterFunction_products(data):
                products = KEY_ARR.getKeyArr()
                for product in products:
                    if data['公司名'] != None:
                        if product in data['公司名']:
                            return True
                    if data['产品'] != None:
                        if product in data['产品']:
                            return True
                    if data['信息'] != None:
                        if product in data['信息']:
                            return True
                return False
            # 从数据库中取出最后一个数据。利用假取得方式
            datas = self.hander.falsePop(databaseName='0_初始客户群', num=1)
            if len(datas)==0:
                PrintTool.print("数据库(database): [0_初始客户群] 为空,无法继续处理数据,正在关闭后续操作...")
                return
            data=datas[0]
            #判断这个数据是否在目标数据库已经存在。
            if self.hander.checkData(databaseName='1_已验客户群',data=data):
                # 根据过滤器过滤掉我们不需要的数据
                if filterFunction_site(data) and filterFunction_products(data):#这个是我们需要的数据。进入function。进行数据处理
                    #在执行机器人的时候，先判断目标数据库有没有该数
                    item=use天眼查Robot(data)#通过天眼查,爬取公司信息
                    if len(item)!=0:
                        newdatas = self.hander.datasZip(keyData=item, data=data)#整合两种信息
                        #由于整合了新数据，因此还要再判断一下是否和目标数据库数据重复了
                        if self.hander.checkData(databaseName='1_已验客户群',data=newdatas):
                            newdatas['_status'] = '经天眼查验证'#加上状态码
                            self.hander.putDatas_setProcessedSign(databaseName='1_已验客户群', datas=[newdatas])
                            self.hander.pop(databaseName='0_初始客户群', num=1)  # 取出原本的数据
                            PrintTool.print("成功存入整合后数据，并存入 数据库(database): [1_已验客户群] " + str(newdatas), fontColor='pink')
                else:
                    if self.hander.checkData(databaseName='无效客户群', data=data):
                        #我们不需要的数据,我们把这些数据丢到无效客户群中
                        self.hander.putDatas_setProcessedSign(databaseName="无效客户群", datas=[data])
                        #确保数据已经丢弃后，我们把原来的数据从原来的数据库中删除掉
                        data = self.hander.pop(databaseName='0_初始客户群', num=1)
            else:
                self.hander.pop(databaseName='0_初始客户群', num=1)
                PrintTool.print("该数据已经存在 数据库(database): [1_已验客户群] |正在丢弃该数据:"+str(data),fontColor='yellow')
        def third_():#发送短信
            pass
        engine=Engine().start()
        #开始任务
        engine.setExecuteTask(name='csvToExcelTask',task=Task(mode='Timing',interval=2,executeNum=-1,
                                                              functionsAndOptions=[
                                                                  first_,secound_
                                                              ]))
        engine.execute('csvToExcelTask')
if __name__ == '__main__':
    Action().main()
    # a=re.compile(r'[\u4e00-\u9fa5_a-zA-Z0-9_]+')
    # print(re.match(a,None).group())


