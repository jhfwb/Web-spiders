#去除掉相同属性的字符串
import os

from clientScrapySystem.webScrapySystem.GYS_pySpiders.utils.dataReadArr import csvFileTool

if __name__ == '__main__':
     #读取配置文件
    print(os.getcwd())
    path= "../../../../Include/scripyData/顺企网_key=吊装带.csv"
    newPath="../../../Include/scripyData/顺企网_key=吊装带.csv"
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