#将数据保存到数据库
from _xhr_tool._utils import TxtTool
from _xhr_tool.mysql.connect import MySqlOptions
import os
if __name__ == '__main__':
    sqlOption=MySqlOptions(host='localhost', user='root', password='512124632', database='crapydatabase')
    fileNames=os.listdir('.')
    fileNames=list(filter(lambda x:x.endswith('.txt'),fileNames))
    txtTool=TxtTool()
    for fileName in fileNames:
        datas=txtTool.readDatas(path=fileName)
        for data in datas:
            sucess=sqlOption.insert(table='company',objDict={'公司':data,'数据状态':'需天眼查查验','数据来源':'人工录入'})
            if sucess==False:
                数据状态=sqlOption.find_tables(table='company',columns=['数据状态'],conditions=[('公司',data)])[1][0]
                if 数据状态=='未知数据':
                    sqlOption.update(table='company',columeName='数据状态',newValue='需天眼查查验',conditions=[('公司',data)])
