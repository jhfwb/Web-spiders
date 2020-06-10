import csv
#去除掉相同属性的字符串
from src.GYS_pySpiders.utils.dataReadArr import csvFileTool

if __name__ == '__main__':
     #读取配置文件
    path="C:/Users/1234567/Desktop/git库存储/Web-spiders/src/GYS_pySpiders/顺企网_key=吊装带.csv"
    newPath="C:/Users/1234567/Desktop/git库存储/Web-spiders/src/GYS_pySpiders/顺企网_key=吊装带.csv"
    attr="公司名"
    csvtool=csvFileTool()
    readArr=csvtool.readCsvData_arrDict(path,encoding='ANSI')
    newArr=[]
    i=1
    for read in readArr:
        sign='unsame'
        for ne in newArr:
            if ne[attr]==read[attr]:
               sign='same'
               break;
        if sign=='unsame':
            newArr.append(read)
    print(len(newArr))
    print(len(readArr))
    csvtool.writeCsvData_arrDict(path=newPath,arr=newArr,encoding='ANSI')