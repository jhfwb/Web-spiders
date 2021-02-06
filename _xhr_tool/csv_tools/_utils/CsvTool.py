import csv
import os
from _xhr_tool._annotate import singleObj


@singleObj
class CsvTool:
    """
    交互csv文件的工具。
    1.读取，存储csv文件
    """
    def getCsvHeader(self,path='',encoding='utf-8'):
        """获得csv文件的行
        :param path: 需要读取的csv文件的路径。
        :param encoding: 以什么编码形式读取文件。
        """
        self._isCsvFile(path)
        with open(path, 'r',encoding=encoding) as fp:
            # encoding是读取时候的解码规则
            line=fp.readline()
            arr=line[0:len(line)-1].split(',')
            return arr
    def _readCsvFileByAllEncodingToArr(self,path='',status=['ANSI','gbk','utf-8']):
        """
        读取csv文件，无论这个csv文件是哪种编码。
        将其转化成数组格式
        """
        if len(status)==0:
            raise UnicodeDecodeError('utf-8,gbk,ANSI这三种编码格式都无法解析')
        encoding=status.pop()
        with open(file=path, mode='r', encoding=encoding) as fp:
            try:
                # encoding是读取时候的解码规则
                readers = csv.DictReader(fp)
                return list(readers)
            except UnicodeDecodeError:
                fp.close()
                return self._readCsvFileByAllEncodingToArr(path=path,status=status)
    def _isCsvFile(self,path):
        path = str(path)
        if path=="":
            raise ValueError('路径为空!!!')
        if not path.endswith('.csv'):
            raise ValueError('文件名必须以.csv为结尾。' + path + '不是以.csv结尾')

    def popLastData(self,path='',isPop=False,encoding='utf-8'):
        """
        :param path: csv的文件路径
        :param isPop: 是否删除文件的最后一个数据，默认不删除。
        :param encoding: 编码

        usage:
            >>>  print(CsvTool().popLastData(path='test.csv',isPop=True))
        当isPop为True的时候，弹出文件末尾的数据
        当isPop为False的时候，获得文件末尾的数据
        """
        self._isCsvFile(path)
        arr=self.optionCsv(path=path,mode='r',encoding=encoding)
        if len(arr)==0:
            raise ZeroDivisionError('无法弹出数据，因为该文件:'+path+',数据为空')
        if isPop==False:
            return arr[len(arr) - 1]
        else:
            data=arr[len(arr) - 1]
            del arr[len(arr) - 1]
            self.optionCsv(path=path,datas=arr,mode='w',encoding=encoding)
            return data
    def optionCsv(self,path='',datas=[],mode="a",encoding='utf-8',isCreateFile=False,outputDatas='arr'):
        """操作csv文件

        usage:
            >>> # 读取文件
            >>>  datas=CsvTool().optionCsv(path='test.csv',mode='r')
            >>> #写入文件
            >>>  CsvTool().optionCsv(path='test.csv',mode='w',datas =[{'name':'张三','age':'12'}],encoding='utf-8')
            >>> #为文件添加数据
            >>>  CsvTool().optionCsv(path='test.csv',mode='a',datas=[{'name':'李四','age':'121'}],encoding='utf-8')

        mode模式介绍:
         * r 读取模式,根据csv文件路径读取datas数据。此时必要参数为path，mode
         * a 添加模式,根据csv文件路径添加datas数据。此时必要参数为path，mode，datas
         * w 写入模式,根据csv文件路径覆写datas数据。此时必要参数为path，mode，datas

        :param path: 操作的csv文件的路径
        :param datas: 数据集。格式必须如此[{name:'张三',age:'19'},{name:'李四',age:'12'}]
        :param mode: 模式。共有r,a,w三种模式
        :param encoding: 编码。1.utf-8  2.ANSI  3.gbk
        :param isCreateFile: 当该文件不存在的时候，是否创建该文件。默认不创建。
        :return:
        """
        self._isCsvFile(path)
        if not os.path.exists(path):
            if isCreateFile:
                if not os.path.exists(os.path.dirname(path)): #如果文件夹不存在，则创建文件夹
                    os.makedirs(os.path.dirname(path))
                f = open(path, "a")
                f.close()
            else:
                raise FileNotFoundError("找不到该文件:"+path)
        if mode=='r':
            return self._readCsvFileByAllEncodingToArr(path=path,status=['ANSI','gbk','utf-8'])
        if mode=='w':
            if len(datas)==0:
                with open(path, 'w', encoding=encoding, newline="") as fp:
                    # encoding是读取时候的解码规则
                    fp.write('')
                    fp.close()
                    return
            headers = list(datas[0].keys())
            with open(path, 'w', encoding=encoding, newline="") as fp:
                # encoding是读取时候的解码规则
                writer = csv.DictWriter(fp, headers)
                writer.writeheader()
                writer.writerows(datas)
        if mode=='a':#弹性添加
            #判断文件存不存在
            if os.path.exists(path):
                #判断是否有header
                oldArr=[]
                with open(path, 'r', encoding=encoding) as fp:
                    # encoding是读取时候的解码规则
                    readers = csv.DictReader(fp)
                    oldArr=list(readers)
                fp.close()
                newDatas=oldArr+datas
                self.optionCsv(path=path, mode='w', encoding=encoding, datas=newDatas)
            else:
                self.optionCsv(path=path,mode='w',encoding=encoding,datas=datas)
            pass
        pass
if __name__ == '__main__':

    print(CsvTool().popLastData(path='test.csv',isPop=True))
    # CsvTool().optionCsv(path='test.csv', mode='a', datas=[{'name': '李四', 'age': '121'}], encoding='utf-8')
    # ExcelTool().optionCsv(path='test.csv',datas=[{'name':'张三','age':333},{'name1':'oso','age':233}])