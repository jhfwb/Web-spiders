import csv
import os


class ExcelTool:
    def optionCsv(self,path='',datas=[],mode="a",encoding='utf-8'):
        if not path.endswith('.csv'):
            raise ValueError('文件名必须以.csv为结尾。'+path+'不是以.csv结尾')
        if mode=='r':
            with open(path, 'r', encoding=encoding) as fp:
                # encoding是读取时候的解码规则
                readers = csv.DictReader(fp)
                return list(readers)
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
    ExcelTool().optionCsv(path='test.csv',datas=[{'name':'张三','age':333},{'name1':'oso','age':233}])