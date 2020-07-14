import os
from utils.RR_Comments import ArrTool, JudgeType, ReflexTool
from utils.excelTool.ExcelTool import ExcelTool
class DatabaseHandler:
    """
    主要实现对数据的增删改查取。
    添加。
    增加：putDatas
    删除：
    弹出数据库数据：pop
    获得数据库所有数据:getAll
    """
    def __init__(self):
        self.excelTool=ExcelTool()
        self.indexKey="公司名"#数据库唯一标识码
        pass
    def datasZip(self,keyData,data):
        keyData=self._makeStandard(keyData)[0]
        data=self._makeStandard(data)[0]
        newData=keyData.copy()
        for key in newData.keys():
            if newData[key]==None or newData[key]=="":
                newData[key]=data[key]
            if key!=self.indexKey:
                if data[key]!=None:
                    if newData[key].strip()!=data[key].strip():
                        newData[key]= str(newData[key])+"|||"+str(data[key])

        return newData
        #

    def pop(self,databseName="",num=1):
        """
        从数据库弹出具体数据。如果这个数量超过数据库所有数据。则会报错
        @param: databaseName str 数据库名字
        @param: num int 弹出的数量
        @return: 返回弹出的数据。
        """
        #获取数据库大小。判断数据库大小是否小于取出数量。如果小于则报错
        if num==-1:
            datas=self.getAll(databseName=databseName)
            excels=self._getExcelFileNameList(dirPath='../database/'+databseName)
            for excel in excels:
                os.remove(excel)
            return datas
        self._getDatabaseStatus()
        lastFENQU=self._getLastFENQUname(databseName=databseName)
        datas=self.excelTool.optionExecl(mode='r',path=lastFENQU)
        if len(datas)>=num:
            dataspop=datas[len(datas)-num:len(datas)]
            if len(datas)==num:#删除这个分区
                os.remove(lastFENQU)
            else:
                self.excelTool.optionExecl(mode='w',path=lastFENQU,datas=datas[0:len(datas) - num])
            self.initDatabase(databseName=databseName)
            return dataspop
        else:
            os.remove(lastFENQU)
            popNum=(num-len(datas))%2000
            cycleTimes=int((num-len(datas))/2000)
            for i in range(cycleTimes):
                lastFENQU = self._getLastFENQUname(databseName=databseName)
                datas = datas+self.excelTool.optionExecl(mode='r', path=lastFENQU)
                os.remove(lastFENQU)
            if popNum>0:
                datas = datas+self.pop(databseName=databseName,num=popNum)
            self.initDatabase(databseName=databseName)
            return datas
    # def filterData(self,datas=[],filterFunction='',option={}):
    #     if JudgeType.getType(filterFunction)!='method' or JudgeType.getType(filterFunction)!='function':
    #         raise ValueError("参数错误，filterFunction必须是可执行函数。")
    #     for
    #     ReflexTool.execute(filterFunction, option)
    #

    def backRollFunction(self,function="",option={},errorFunction="",errorOption={}):
        if JudgeType.getType(function)!='method' or JudgeType.getType(function)!='function':
            raise ValueError("参数错误，function必须是可执行函数。")
        if JudgeType.getType(errorFunction)!='method' or JudgeType.getType(function)!='function':
            raise ValueError("参数错误，errorFunction必须是可执行函数。")
        try:
            ReflexTool.execute(function,option)
        except:
            ReflexTool.execute(errorFunction,errorOption)
        pass
    def putDatas(self,databseName="",datas=[],filter=None):#在末尾添加数据。推荐使用，比较省时间。
        """
        将数据数据保存到数据库中。
        1.将需要存入的数据进行排序，并根据关键词去重。
        1.获得数据库中的索引
        2.过滤掉与数据库相同的数据
        3.

        @param:databseName| str 存入的数据库名称
        @param:datas| [] 需要存入数据库的数据组
        @param:key| str 存入时候的键值
        """
        #去除到公司名为None的数据
        if len(datas)==0:
            return None
        datas = self._makeStandard(datas=datas)  # 数据标准化。
        datas=list(filter(lambda x:x!=None,datas))
        datas = list(filter(lambda x: x.get(self.indexKey) != None, datas))
        datas=ArrTool.removeRepeat(arr=datas,keyFunction=lambda x:x.get(self.indexKey))#自身去重
        indexsNames=self._getDatabaseIndexs(databseName=databseName)#取索引
        datas=list(filter(lambda x:not x[self.indexKey] in indexsNames,datas))#索引去重
        self._writeDatasIntoFENQU(databseName=databseName,datas=datas)#将数据写入扇区
        self.initDatabase(databseName=databseName)#重新初始化数据库
        return datas
    def _writeDatasIntoFENQU(self,databseName="",datas=[]):
        if len(datas)==0:
            return
        datas=self._makeStandard(datas=datas)
        lens = len(datas)
        if lens!=0:
            FENQU=self._getLastFENQUname(databseName=databseName)
            if FENQU==None:
                cycle = int(lens / 2000) + 1
                num = 1
                # self.excelTool.optionExecl(mode='w', datas=databseDatas,
                #                            path='../database/' + databseName + '/分区' + str(++num) + '.xlsx')
                for i in range(cycle):
                    self.excelTool.optionExecl(mode='w', datas=datas[2000 * i:(2000 * i + 2000)],
                                               path='../database/' + databseName + '/分区' + str(num) + '.xlsx')
                    num += 1
            else:
                oldDatas = self.excelTool.optionExecl(mode='r', path=FENQU)
                shengyu = 2000 - len(oldDatas)
                if shengyu - len(datas) >= 0:  # 刚刚好，直接加进去
                    self.excelTool.optionExecl(mode='w', path=FENQU, datas=oldDatas + datas)
                else:
                    self.excelTool.optionExecl(mode='w', path=FENQU, datas=oldDatas + datas[0:shengyu])
                    datas=datas[shengyu:len(datas)]
                    cycle = int(len(datas) / 2000) + 1
                    num = int(FENQU[len(FENQU) - 6])+1
                    # self.excelTool.optionExecl(mode='w', datas=databseDatas,
                    #                            path='../database/' + databseName + '/分区' + str(++num) + '.xlsx')
                    for i in range(cycle):
                        self.excelTool.optionExecl(mode='w', datas=datas[2000 * i:(2000 * i + 2000)],
                                                   path='../database/' + databseName + '/分区' + str(num) + '.xlsx')
                        num += 1
    def _getLastFENQUname(self,databseName=""):
        excels=self._getExcelFileNameList(dirPath=self._getDatabasePath(databseName=databseName))
        if len(excels)==0:
            return None
        mid=-1
        for excel in excels:
            print(excel)
            mun=int(excel[len(excel) - 6])
            if mun>mid:
                mid=mun
        return '../database/'+databseName+'/分区'+str(mid)+".xlsx"
    def initDatabase(self, databseName=""):
        """
        初始化数据库。
        @param databaseName:数据库名称
        @param key:添加关键词。

        初始化数据库:
        1.创建状态文件:
            size:数据数量
        2.创建索引文件:根据key来创建
        """
        # 删除掉两个文件：
        databsePath = self._getDatabasePath(databseName)
        os.remove(databsePath + '/index.txt')
        datas = self.getAll(databseName=databseName)
        # 重新创建索引文件
        fp1 = open(mode='w', file=databsePath + '/index.txt', encoding='utf-8')
        # 读取index
        lines = []
        for data in datas:
            lines.append(str(data[self.indexKey]) + '\n')
        fp1.writelines(lines)
        fp1.close()
        # 重新创建status文件。
        fp = open(file=databsePath + '/status.txt', mode='w', encoding='utf-8')
        fp.write("size=" + str(len(datas)) + '\n')
        fp.close()
    def getAll(self,databseName=""):
        """
        获得数据库中所有数据。
        :param databseName|str 数据库名称
        """
        # if dirPath!="" and databseName=="":
        #     xlsxFiles=self._getExcelFileNameList(dirPath=dirPath)
        # elif databseName!="" and dirPath=="":
        #     xlsxFiles=self._getExcelFileNameList(dirPath="../database/"+databseName)
        # else:
        #     raise ValueError("参数databseName与参数dirPath不可以同时赋值，或者同时不赋值，会产生冲突。只允许其中一个赋值")
        xlsxFiles = self._getExcelFileNameList(dirPath='../database/'+databseName)
        datas=[]
        for xlsxFile in xlsxFiles:
            data=self.excelTool.optionExecl(path=xlsxFile,mode='r')
            datas=datas+data
        return datas
    def transfer(self,FromDatabseName="",ToDatabaseName="",num=1):
        return self.putDatas(databseName=ToDatabaseName,datas=self.pop(databseName=FromDatabseName,num=num))
    #次要方法
    #X
    # def setDatas(self,databseName="",datas=[],key="公司名"):#Gengg修改数据库。最好不要用，否则有风险哦！！
    #     if len(datas)==0:
    #         return
    #     datas=self._makeStandard(datas)
    #     databseDatas=self.getAll(databseName=databseName)
    #     dataSite=[]
    #     for j in range(len(datas)):
    #         sign=0
    #         for i in range(len(databseDatas)):
    #             if databseDatas[i][key]==datas[j][key]:
    #                 databseDatas[i]=datas[j]
    #                 dataSite.append(i)
    #                 sign=1
    #                 break
    #         if sign==0:
    #             databseDatas.append(datas[j])
    #     #清空数据库，然后重新写入数据。
    #     excelFileNameList=self._getExcelFileNameList(dirPath='../database/'+databseName)
    #     for excelFileNameLis in excelFileNameList:
    #         os.remove(excelFileNameLis)
    #     #重新写入数据
    #     self._writeDatasIntoFENQU(databseName=databseName,datas=databseDatas)
    # def save(self,databseName="",datas="",filePath="",key="公司名"):#单条信息，文件信息都可以储存。
    #     if filePath!="" and datas=="":
    #         excelData=self.excelTool.optionExecl(path=filePath,mode='r')
    #     if filePath=="" and datas!="":
    #         excelData=datas
    #     if filePath != "" and datas != "":
    #         raise ValueError("无法同时以datas与filePath的形式储存数据")
    #     if filePath == "" and datas == "":
    #         raise ValueError("datas，filePath为空。")
    #     if databseName == "":
    #         raise ValueError("databaseName为空")
    #     #使得数据标准化
    #     standardDatas=self._makeStandard(datas=excelData)
    #     #获取数据库信息
    #     #判断当前数据库是否发生变化
    #     if self._judgeDatabaseIsChange(databseName=databseName):
    #         #重新初始化数据库(初始化状态文件，初始化索引文件，自身数据库去重)
    #         self.initDatabase(databseName=databseName)
    #     #自身去重
    #     spliteReSelfDatas=self._splitRepeateSelf(standardDatas)
    #     #获取本数据库中的索引。
    #     indexKeys=self._getDatabaseIndexs(databseName=databseName,key=key)
    #     #根据索引剔除掉重复的数据
    #     spliteReDatas=self._cutDataByIndexkey(datas=spliteReSelfDatas,indexkeys=indexKeys,key=key)
    #     #将数据添加到数据库。250000
    #         #获取数据库中文件大小
    #     #储存数据到分区
    #     self._writeDatasIntoFENQU(databseName=databseName,datas=spliteReDatas)
    # def _judgeDatabaseIsChange(self,databseName=""):
    #     currerntSize = self._getCurrrentDatabaseSize(databseName=databseName)
    #     size = self._getDatabaseStatus(databseName=databseName, key="size")
    #     return not currerntSize==size
    # def _getCurrrentDatabaseSize(self, databseName=""):
    #     ExcelFileNameLists = self._getExcelFileNameList(dirPath='../database/' + databseName)
    #     size = 0
    #     for ExcelFileNameList in ExcelFileNameLists:
    #         size = size + os.stat(ExcelFileNameList).st_size
    #     return str(size)
    def _getDatabaseStatus(self,databseName="",key=""):
        """
        获得数据库状态。
        @param:databaseName | str 数据库名称
        @param:key | str 需要获取的状态关键字
        """
        fileName=self._getDatabasePath(databseName+'/status.txt')
        if  not os.path.exists(fileName):
            fp=open(file=fileName,mode='w',encoding='utf-8')
            fp.write("size="+str(len(self._getDatabaseIndexs(databseName=databseName)))+'\n')
            fp.close()
        fp=open(file=fileName,mode='r',encoding='utf-8')
        lines=fp.readlines()
        for line in lines:
            if line.split('=')[0].strip()==key:
                return line.split('=')[1].strip()
        return None
    # def _cutDataByIndexkey(self,datas=[],indexkeys=[],key=""):
    #     return list(filter(lambda data:data[key] not in indexkeys,datas))
    def _getDatabasePath(self,databseName=""):
        return '../database/'+databseName
    def _getDatabaseIndexs(self,databseName=""):
        """
        获得数据库索引。如果没有这个索引，则会自动创建一个索引文件。
        """
        indexPath=self._getDatabasePath(databseName)+'/index.txt'
        if not os.path.exists(indexPath):
            fp=open(mode='w',file=indexPath,encoding='utf-8')
            #读取index
            lines=[]
            datas=self.getAll(databseName=databseName)
            for data in datas:
                lines.append(data[self.indexKey]+'\n')
            fp.writelines(lines)
            fp.close()
        fp=open(mode='r',file=indexPath,encoding='utf-8')
        lines=fp.readlines()
        lines=map(lambda x:x.strip(),lines)
        return list(lines)
        # self._getExcelFileNameList(dirPath=self._getDatabasePath(databseName=databseName))
    # def _splitRepeateSelf(self,datas,key="公司名"):
    #     newDatas=[]
    #     for data in datas:
    #         sign=0
    #         for newData in newDatas:
    #             if newData[key]==data[key]:
    #                 sign=1
    #         if sign==0:
    #             newDatas.append(data)
    #     return newDatas
    def _makeStandard(self,datas=[]):
        if len(datas)==0:
            return
        excel_standard_hands = self.excelTool.getHeader(path="../template/customerData_template.xlsx")
        if not type(datas)==type([]):
            datas=[datas]
        ks=list(datas[0].keys())
        if not ks==excel_standard_hands:
            newdatas=[]
            for data in datas:
                newData = {}
                newHandArr=excel_standard_hands.copy()
                for i in range(len(newHandArr)):
                    newData.setdefault(newHandArr[i],None)
                keys=data.keys()
                for key in keys:
                    standardKey=self._change_standard_key_same(key,excel_standard_hands,newData)
                    if standardKey:
                        newData[standardKey]=data[key]
                for key in keys:
                    standardKey=self._change_standard_key(key,excel_standard_hands,newData)
                    if standardKey:
                        newData[standardKey]=data[key]
                newdatas.append(newData)
            return newdatas
        return datas
    def _change_standard_key_same(self, key, excel_standard_hands, data):

        for excel_standard_hand in excel_standard_hands:
            try:
                if data[excel_standard_hand] == None:
                    if excel_standard_hand == key:
                        return excel_standard_hand
            except:
                return None
        return ""
    def _change_standard_key(self,key,excel_standard_hands,data):
        for excel_standard_hand in excel_standard_hands:
            try:
                if data[excel_standard_hand]==None:
                    if excel_standard_hand in key:
                        return excel_standard_hand
            except:
                return None
        return ""
    def _getExcelFileNameList(self,dirPath=""):
        """
        获得文件夹中所有的excel文件名称列表，并返回它。
        @param: path:需要查找的文件夹路径
        """
        fileNames=[]
        for root, dirs, files in os.walk(dirPath):
            for file in files:
                if  file.endswith('.xlsx'):
                    fileNames.append(dirPath+'/'+file)
        return fileNames


if __name__ == '__main__':
    # save(databseName='allCustomer', filePath='../smelter/顺企网_key=吊装带.xlsx')
    # datas=DatabaseHandler().pop(databseName='allCustomer',num=3)
    a=DatabaseHandler().transfer(FromDatabseName='allCustomer',ToDatabaseName='0_初始客户群',num=1)
    print(a)
    #增
    #删
    #改。