from clientScrapySystem.DatabaseSystem.src.FilterData import FilterData
from utils.RR_Comments import PrintTool, ArrTool


class DatesTransfer:
    """
    拦截器
    """
    def __init__(self,databaseHandler,fromDatabse,toDatabases,num=1):
        self.fromDatabse=fromDatabse
        self.databaseHandler=databaseHandler
        self.num=num
        self.toDatabases=toDatabases
    def checkLastData(self,databaseName):
        """
        判断数据库中最后一个数据可否被处理，如果可以，返回这个数，如果不可以返回None
        """
        data = self.databaseHandler.falsePop(databaseName=databaseName, num=1)
        if data == None:
            return None
        if type(data)==type([]):
            data=data[0]
        # 判断此数据是否合法。如果不合法则退出此方法
        if not self.databaseHandler.dataIsLegal(databaseName=databaseName, data=data):
            PrintTool.print("该数据不合法。可能是由于该数据已经被重复执行:" + str(data),LogPath=PrintTool.LogPath)
            return None
        return data

        # 判断数据是否合法，
        # 判断数据是否已经存入数据中心。如果没有的话则存入。

        pass
    @staticmethod
    def fun_template(data):
        """
        请将toDatabases中的数据放在对应位置。
        第一个位置：也就是0。放在需要
        第二个位置：
        """
        # 判断data属于哪个客户群
        #不过滤的类型：
        if len(data.values())-ArrTool.getNoneLen(data.values())<4:
            print('这个数据需要返回0')
            return 0
        if FilterData.filterFunction_products(data) == None:
            return 1
        if FilterData.filterFunction_site(data) == None:
            return 2
        if FilterData.filterFunction_company_status(data) == None:
            return -1
        return 0
    def putDataFilter(self,function,datas,ToDatabaseName):
        """
        将这些数据以过滤的形式放到数据库中
        """
        statusAndDatas = {}  # 创建状态数据组
        for data in datas:
            #判断这个数据的键值个数
            #获得数组
            NoneLen=ArrTool.getNoneLen(list(data.values()))
            if NoneLen/len(list(data.values()))>=2:
                status=0
            else:
                status = function(data)  # 执行过滤方法
            if statusAndDatas.get(status) == None:
                statusAndDatas.setdefault(status, [data])
            else:
                statusAndDatas.get(status).append(data)
            try:
                self.toDatabases[status]
            except IndexError:
                raise IndexError('无法识别方法:' + str(function) + '的返回值。')
        for key in statusAndDatas.keys():
            statusAndDatas[key] = self.databaseHandler._addDataToDataCenter(statusAndDatas[key], self.fromDatabse,self.toDatabases[key])  # 修改数据中心值，并返回可修改的值
            if len(statusAndDatas[key])!=0:
                self.databaseHandler.putDatas(databaseName=self.toDatabases[key], datas=statusAndDatas[key])
                PrintTool.print('DatabaseCenter:成功转移数据' + str(
                    len(statusAndDatas[key])) + '条:从[' + self.fromDatabse + ']到[' + self.toDatabases[
                                    key] + ']。以下是转移的数据:' + str(statusAndDatas[key]),
                                fontColor='green',LogPath=PrintTool.LogPath)
    def transferFilter(self,function):#经过过滤的transger。转移的时候必须判断
        if self.databaseHandler.isEmpty(self.fromDatabse):
            PrintTool.print("DatabaseCenter:数据库[" + self.fromDatabse + "]为空,无法转移数据",LogPath=PrintTool.LogPath)
            return None
        datas =  self.databaseHandler.falsePop(databaseName=self.fromDatabse, num=self.num)#取出数据
        self.putDataFilter(function, datas,self.toDatabases)
        return self.databaseHandler.pop(databaseName=self.fromDatabse, num=self.num)

if __name__ == '__main__':
    # def fun(data):
    #     if data['你']==11:
    #         return True
    # data={'你':1,'我':2}
    # print(DatesTransfer().transfer(fun))
    pass