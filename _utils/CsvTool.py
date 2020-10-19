import csv
import os


class CsvTool:
    def getHeader(self,path='',encoding='utf-8'):
        """
        获得csv文件的行
        """
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




    def optionCsv(self,path='',datas=[],mode="a",encoding='utf-8'):
        if not path.endswith('.csv'):
            raise ValueError('文件名必须以.csv为结尾。'+path+'不是以.csv结尾')
        if mode=='r':
            return self._readCsvFileByAllEncodingToArr(path=path,status=['ANSI','gbk','utf-8'])
        if mode=='w':
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
    try:
        assert 1/0
        print(333)
    except:
        print("ihao")
    pass
    # ExcelTool().optionCsv(path='test.csv',datas=[{'name':'张三','age':333},{'name1':'oso','age':233}])