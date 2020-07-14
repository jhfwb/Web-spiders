import time

from clientScrapySystem.DatabaseSystem.src.CsvToXlsx import CsvToXlsx
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
        def secound_():
            data = self.hander.pop(databseName='0_初始客户群', num=1)#原本的信息
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
            # if datas!=None:
            #     datas = self.hander.transfer(FromDatabseName='smelter', ToDatabaseName='0_初始客户群', num=-1)
            # else:
            #     print(2)

        #启动引擎
        # chang()
        engine=Engine().start()
        #开始任务
        engine.setExecuteTask(name='csvToExcelTask',task=Task(mode='Timing',interval=3,executeNum=-1,
                                                              functionsAndOptions=[
                                                                  first_,secound_
                                                              ]))

        engine.execute('csvToExcelTask')
if __name__ == '__main__':
    Action().main()