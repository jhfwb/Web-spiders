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
            bol=CsvToXlsx().working()
            datas=self.hander.transfer(FromDatabseName='smelter',ToDatabaseName='0_初始客户群',num=-1)
            #启动机器人吧。可以开始验证了
        def secound_():#将数据从0中取出来，并
            def erroFunction(data):
                PrintTool.print(s="数据发生异常:已经回滚数据"+data)
                self.hander.putDatas(databseName='0_初始客户群',datas=data)
            def functon(data):
                self.天眼查.run(self.con.robotThread, data[0]['公司名'])
                items=self.con.robotThread.itemsQueue.get()#爬取的信息
                if type(items['手机'])==type([]):
                    line=""
                    for phone in items['手机']:
                        line+=phone+"|||"
                    items['手机']=line[0:len(line)-3]
                newdatas=self.hander.datasZip(keyData=items,data=data[0])
                newdatas['_status']='经天眼查验证'
                self.hander.putDatas(databseName='1_已验客户群',datas=[newdatas])
                PrintTool.print("成功存入整合后数据，并存入数据库:1_已验客户群"+str(newdatas),fontColor='pink')
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
            data = self.hander.pop(databseName='0_初始客户群', num=1)#取出原本的数据
            #引入过滤器，对数据进行过滤
            if filterFunction_site(data) and filterFunction_products(data):# 获取位置以及产品我们需要的
                self.hander.backRollFunction(functon=functon, option={'data': data}, errorFunction=erroFunction,
                                             errorOption={'data': data})
            else:#我们不需要的数据
                self.hander.putDatas(databseName="无效客户群", datas=data)




        #启动引擎
        # chang()
        engine=Engine().start()
        #开始任务
        engine.setExecuteTask(name='csvToExcelTask',task=Task(mode='Timing',interval=0,executeNum=1,
                                                              functionsAndOptions=[
                                                                  first_,secound_
                                                              ]))

        engine.execute('csvToExcelTask')
if __name__ == '__main__':
    Action().main()
