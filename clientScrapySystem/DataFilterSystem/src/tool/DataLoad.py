# 将文件数据转化成内存。
# 文件夹位置
import os

from clientScrapySystem.chromeRobotSystem.utils.excelTool.dataReadArr import csvFileTool


class DataHander:
    """
    1.读取srcFile文件夹的csv数据，并保存到内存中
    """
    srcFilePaths=[] # 处理的原始文件名称集合。
    srcDirPath='srcFile/'
    garbagePath='dealFiles/'
    #C:\Users\1234567\Desktop\git库存储\Web-spiders\clientScrapySystem\DataFilterSystem\srcFile\顺企网2020-10-12.csv
    def __init__(self):
        self.csvTool=csvFileTool()
        self.datas=self.loadDatas()
    def loadDatas(self):
        # 获得srcFile文件下面的csv文件。
        files=os.listdir(self.srcDirPath)
        datasArr=[]
        for fileName in files:
            if fileName.endswith('.csv'):
                self.srcFilePaths.append(fileName)
                datas = self.csvTool.readCsvData_arrDict(path=DataHander.srcDirPath + fileName,
                                                            encoding='gbk')
                datasArr.append(datas)
        return datasArr
    def saveDatas(self,datas=[],fileNameSign='_',fileName=''):
        """
        将参数datas中的数据保存成csv文件。
        保存的文件名为参数srcFilePath的文件名并且后面加上后缀fileNameSign
        比如:srcFilePath=test.csv
        参数fileNameSign=_你好
        则最终保存的文件名称为  test_你好.csv
        保存的文件夹路径为参数srcDirPath所对应的值
        """
        if len(datas)==0:
            return
        self.csvTool.writeCsvData_arrDict(path=DataHander.garbagePath+self._addAfterName(name=fileName,afterName=fileNameSign),encoding='gbk',arr=datas)
    def _addAfterName(self,name='',afterName=''):
        """
        添加或追。
        假设name的值为‘你好.csv’
        当调用addAfterName(self,name='你好.csv',afterName='_1')的时候
        返回的结果为 你好_1.csv
        如果name的后缀部位csv，则返回原值即你好.csv
        """
        if not name.endswith('.csv'):
            return name
        name=name[0:len(name)-4]+afterName+'.csv'
        return name


# if __name__ == '__main__':
    # DataHander().addAfterName(name='你好.csv',afterName='11')




