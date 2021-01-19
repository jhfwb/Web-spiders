#coding:utf-8
from clientScrapySystem.DatabaseSystem.src.CsvToXlsx import CsvToXlsx
from clientScrapySystem.DatabaseSystem.src.DatesTransfer import DatesTransfer
from clientScrapySystem.DatabaseSystem.utils.DatabaseHandler import DatabaseHandler
from clientScrapySystem.DatabaseSystem.utils.Engine import Engine, Task
from clientScrapySystem.chromeRobotSystem.Context import Context
from clientScrapySystem.chromeRobotSystem.天眼查 import 天眼查
from _xhr_tool._utils.RR_Comments import PrintTool, StringTool


class Action:
    def main(self):
        self.con=Context()
        self.con.main()
        self.hander=DatabaseHandler()
        self.天眼查=天眼查()
        self.datesTransfer=DatesTransfer(databaseHandler=self.hander,fromDatabse='smelter',
                          toDatabases=['0_初始客户群','其他产品客户群','其他区域客户群'],num=1)

        def first_():# 监听smelter中有没有数据。将smelter中的csv文件转成xlsx文件。并转存到0_初始客户群的数据库中
            PrintTool.print('=========================程序开始运行====================', fontColor='gray', LogPath=PrintTool.LogPath)
            PrintTool.print('first_方法开始执行!',fontColor='gray', LogPath=PrintTool.LogPath)
            bol=CsvToXlsx().working2()
            # 将semlter所有数据转移过去。如果在中央数据库已经存在的数据，则不会被转移过去。
            DatesTransfer(databaseHandler=self.hander,fromDatabse='smelter',
                          toDatabases=['0_初始客户群','其他产品客户群','其他区域客户群'],num=-1).\
                        transferFilter(DatesTransfer.fun_template)
            #bug测试中........
            ##测试任务
            # 1.数据能否达到其功能
            # 2.能否正常转移数据。
            # 3.能否能够按照过滤器转移数据
            # 4. 重复数据是否会剔除
            assert 1/0 
        #启动机器人吧。可以开始验证了。
        def secound_():#将数据从0中取出来，并
            def use天眼查Robot(data):#经过天眼查处理，获得的天眼查数据
                self.天眼查.run(self.con.robotThread, data['公司名'])
                items=self.con.robotThread.itemsQueue.get()#爬取的信息
                if items=="正常终止ACTION":
                    return items
                elif items=="异常终止ACTION":
                    return items
                else:
                    if items.get("手机")!=None:
                        if type(items['手机'])==type([]):
                            line=""
                            for phone in items['手机']:
                                line+=phone+"|||"
                            items['手机']=line[0:len(line)-3]
                    return items
            PrintTool.print('secound_方法开始执行!', fontColor='gray', LogPath=PrintTool.LogPath)
            # 判断这个数据库中最后一个数据能否被处理。能的话则返回data。不能的话返回None
            data=self.datesTransfer.checkLastData(databaseName='0_初始客户群')
            #将数据添加到数据中心
            if data==None:
                return
            PrintTool.print('正在使用天眼查查询公司数据:'+data['公司名'], fontColor='gray',LogPath=PrintTool.LogPath)
            # self.hander._addDataToDataCenter(data,'0_初始客户群','0_初始客户群')
            item = use天眼查Robot(data)  # 通过天眼查,爬取公司信息
            if item == "正常终止ACTION":
                self.hander.putDatas_setProcessedSign(databaseName="回收站", datas=[data])
                self.hander.pop(databaseName='0_初始客户群', num=1)
            elif item == "异常终止ACTION":
                self.hander.putDatas_setProcessedSign(databaseName="程序异常客户群", datas=[data])
                self.hander.pop(databaseName='0_初始客户群', num=1)
            else:
                if StringTool.getSameLevel(item[self.hander.indexKey], data[self.hander.indexKey]) > 0.6:#相似。不相似。
                    newdatas = self.hander.datasZip(keyData=item, data=data)  # 整合两种信息
                    #这是新数据诞生。要确认该信息是否存在
                    if self.hander.checkData(databaseName='1_已验客户群', data=newdatas):
                        newdatas['_status'] = '经天眼查验证'  # 加上状态码
                        self.hander.putDatas_setProcessedSign(databaseName='1_已验客户群', datas=[newdatas])
                        self.hander.pop(databaseName='0_初始客户群', num=1)  # 取出原本的数据
                        PrintTool.print("成功存入整合后数据，并存入 数据库(database): [1_已验客户群] " + str(newdatas),
                                        fontColor='pink')
                    else:
                        self.hander.pop(databaseName='0_初始客户群', num=1)  # 取出原本的数据
                else:
                    #不相似，丢到垃圾桶

                    pass
            #
            #     # 根据一级过滤器过滤掉我们不需要的数据
            #     if filterFunction_site(data) and filterFunction_products(data):#这个是我们需要的数据。进入function。进行数据处理
            #         #在执行机器人的时候，先判断目标数据库有没有该数
            #         item=use天眼查Robot(data)#通过天眼查,爬取公司信息
            #         #启动二级过滤，过滤掉天眼查查询后我们不需要的信息
            #         if item == "正常终止ACTION":
            #             self.hander.putDatas_setProcessedSign(databaseName="回收站", datas=[data])
            #             self.hander.pop(databaseName='0_初始客户群', num=1)
            #         elif item == "异常终止ACTION":
            #             self.hander.putDatas_setProcessedSign(databaseName="程序异常客户群", datas=[data])
            #             self.hander.pop(databaseName='0_初始客户群', num=1)
            #         else:
            #             if filterFunction_company_status(item):
            #                 #比较两条信息是否相同。如果不相同
            #                 if StringTool.getSameLevel(item[self.hander.indexKey],data[self.hander.indexKey])>0.6:
            #                     newdatas = self.hander.datasZip(keyData=item, data=data)#整合两种信息
            #                     if self.hander.checkData(databaseName='1_已验客户群', data=newdatas):
            #                         newdatas['_status'] = '经天眼查验证'  # 加上状态码
            #                         self.hander.putDatas_setProcessedSign(databaseName='1_已验客户群', datas=[newdatas])
            #                         self.hander.pop(databaseName='0_初始客户群', num=1)  # 取出原本的数据
            #                         PrintTool.print("成功存入整合后数据，并存入 数据库(database): [1_已验客户群] " + str(newdatas),
            #                                         fontColor='pink')
            #                     else:
            #                         self.hander.pop(databaseName='0_初始客户群', num=1)  # 取出原本的数据
            #                 else:
            #                     self.hander.putDatas_setProcessedSign(databaseName="回收站", datas=[data])
            #                     self.hander.pop(databaseName='0_初始客户群', num=1)
            #
            #                 #由于整合了新数据，因此还要再判断一下是否和目标数据库数据重复了
            #             else:
            #                 self.hander.putDatas_setProcessedSign(databaseName="回收站", datas=[data])
            #                 self.hander.pop(databaseName='0_初始客户群', num=1)
            #     else:
            #         print("其他区域处理")
            #         if self.hander.checkData(databaseName='其他区域客户群', data=data):
            #             #我们不需要的数据,我们把这些数据丢到无效客户群中
            #             self.hander.putDatas_setProcessedSign(databaseName="其他区域客户群", datas=[data])
            #             #确保数据已经丢弃后，我们把原来的数据从原来的数据库中删除掉
            #             data = self.hander.pop(databaseName='0_初始客户群', num=1)
            # else:
            #     self.hander.pop(databaseName='0_初始客户群', num=1)
            #     PrintTool.print("该数据已经存在 数据库(database): [1_已验客户群] |正在丢弃该数据:"+str(data),fontColor='yellow')
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


