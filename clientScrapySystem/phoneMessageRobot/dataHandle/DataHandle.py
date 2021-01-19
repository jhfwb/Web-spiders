import re as re1
from clientScrapySystem.phoneMessageRobot.dataHandle.utils.dataReadArr import csvFileTool
class DataHandle:
    """
    用于处理数据
    """
    def __init__(self):
        self.dataHandler = csvFileTool()
        pass

    def dataHandle(self, inputPath='', outputPath='send.csv',keys=[],idkey=''):
        path1 = self.csv_execCode(inputPath=inputPath)  # 生成执行文件
        path1=self.csv_pickDataByKey(inputPath=path1, keys=keys)  # 生成发送文件
        path1=self.csv_addLine(inputPath=path1,header='time',data='0')
        self.csv_removeRepeatByKey(inputPath=path1,key=idkey,outputPath=outputPath)
        return self.dataHandler.readCsvData_arrDict(outputPath)

    def csv_addLine(self,inputPath='',outputPath='',header="",data=""):
        dics=self.dataHandler.readCsvData_arrDict(inputPath)
        # dic=list(map(lambda x:x.setdefault(header,data); return x;,dic))
        for i in range(len(dics)):
            dics[i].setdefault(header,data)
        if outputPath=="":
            outputPath=inputPath.replace('.csv','_add'+header+'.csv')
        self.dataHandler.writeCsvData_arrDict(path=outputPath,arr=dics)
        return outputPath

    def csv_execCode(self, inputPath='', outputPath=''):
        """
        对csv文件的源数据进行处理，并对每条数据执行表头算法的数据。

        eg:
            >>> DataHandle().csv_execCode(inputPath='test.csv')
                    ↓-------test.csv -------↓
                    公司名,"客户{{customer=customer[0]+'总'}}(re='.{2,3}')",手机号{{phone}}(re='\d{11}'),"{{message='尊敬的'+customer+',您好!'}}"
                    百宏聚纤科技有限公司,吴金錶,13700000001
                    百宏聚纤科技有限公司,施天佑,1370000000
                    百宏聚纤科技有限公司,哈,1370000000
                    ↑-------test.csv-------↑
            转化后：
                    ↓-------test_execCode.csv -------↓
                        customer,phone,message
                        吴总,13700000001,"尊敬的吴总,您好!"
                    ↑-------test_execCode.csv-------↑
                    ↓-------test_execCode_err.csv -------↓
                        customer，phone，message
                        吴总，13700000001，尊敬的吴总，您好
                    ↑-------test_execCode_err.csv-------↑

        例如源文件是 aa.csv
        处理后：aa_1_excCode.csv
        并且会生成错误的文件：aa_1_excCode_erro.csv
        生成的文件默认同级
        :param inputPath: 文件路径
        :return:path: 存储的文件名称
        """
        if inputPath.endswith('.csv') == False:
            raise NameError('请确保传入的inputPath是csv文件~~~୧(๑•̀◡•́๑)૭')
        # 获得原始数据的数组
        srcDatas = self.dataHandler.readCsvData_arrArr(inputPath) #srcDatas-从inputPath文档中获得的内存数据。是一个集合
        header = [] # header-新数据的表头
        headerHandles = [] # headerHandles-存放执行代码
        removeHeader=[]
        # 为header与headerHandles存入其值。
        for i in range(0, len(srcDatas[0])):
            reArr = re1.findall(r'\{\{(.*)\}\}', srcDatas[0][i])
            reCheckArr = re1.findall(r'\(\(re=(.*)\)\)', srcDatas[0][i])
            if len(reArr) > 0:
                if reArr[0].split('=')[0].startswith('!'):
                    removeHeader.append(reArr[0].split('=')[0][1:])
                    header.append(reArr[0].split('=')[0][1:])
                else:
                    header.append(reArr[0].split('=')[0])
                if len(reCheckArr) > 0:
                    if (reCheckArr[0].startswith('\'') and reCheckArr[0].endswith('\'')) or (
                            reCheckArr[0].startswith('\"') and reCheckArr[0].endswith('\"')):
                        reCheckArr[0] = reCheckArr[0][1:len(reCheckArr[0]) - 1]
                    print((i, reArr[0], reCheckArr[0]))
                    headerHandles.append((i, reArr[0], reCheckArr[0]))
                else:
                    headerHandles.append((i, reArr[0], ''))
        datas = []  # 获得缩小后的范围
        # 先限定大小：
        for i in range(1, len(srcDatas)): #获得初始值
            arr = []
            for headerHandle in headerHandles:
                if headerHandle[0] >= len(srcDatas[i]):
                    arr.append('')
                else:
                    arr.append(srcDatas[i][headerHandle[0]])
            datas.append(arr) #

        headerHandles = list(map(lambda x: (x[1], x[2]), headerHandles)) # 保存执行语句
        datasErro = []
        locVab={} #本地变量 用于储存exe中的返回值。
        locEnv={} #本地环境 将一个作用域表示成一个对象。
        for index in range(0, len(datas)): #开始执行语句，并赋值
            for j in range(0, len(datas[index])):
                de = headerHandles[j][0].split('=')[0]
                # tool.print(datas[index][j],fontColor='yellow')
                a = None
                if headerHandles[j][1] != '':
                    a = re1.fullmatch(headerHandles[j][1], datas[index][j].strip())
                else:
                    a = ''
                if a == None:
                    datasErro.append(srcDatas[index+1]) #
                    datas[index] = None
                    break
                if de.startswith('!'):
                    de=de[1:]
                exec(de + '="' + datas[index][j].strip() + "\"",locEnv,locVab)
                try:
                    if headerHandles[j][0].startswith('!'):
                        exec(headerHandles[j][0][1:],locEnv,locVab)
                    else:
                        exec(headerHandles[j][0], locEnv, locVab)
                    datas[index][j] = locVab[de]
                except:
                    raise ValueError(headerHandles[j][0] + "执行失败。未成功添加。请确保语法正确")
        # 检查每一条数据的准确性
        datas = list(filter(lambda x: x != None, datas))
        # 输出：
        if outputPath == '':
            outputPath = inputPath.replace('.csv', '_excCode.csv')


        removeHeaderI=removeHeader.__iter__()
        removeId=[]
        while True:
            try:
                each = next(removeHeaderI)
                for i in range(len(header)):
                    if header[i]==each:
                        removeId.append(i)
                        del header[i]
                        break
            except StopIteration:
                break
        # print(header)
        # print(removeId)
        for i in range(len(datas)):
            for remove in removeId:
                del datas[i][remove]
            # for j in range(len(datas[i])):
            #     for remove in removeId:
            #         print(datas[i][remove])
            #         del datas[i][remove]

        self.dataHandler.writeData_arrArr(outputPath, header=header, datas=datas)
        self.dataHandler.writeData_arrArr(outputPath.replace('.csv', '_erro.csv'), header=srcDatas[0], datas=datasErro)
        return outputPath

    def csv_pickDataByKey(self, inputPath='', outputPath='', keys=[]):
        arr = self.dataHandler.readCsvData_arrDict(inputPath)
        newArr = []
        for i in range(0, len(arr)):
            obj = {}
            for key in keys:
                try:
                    obj.setdefault(key, arr[i][key])
                except:
                    raise ValueError('在' + inputPath + "文件中，不存在该表头" + key)
            newArr.append(obj)
        if outputPath == '':
            outputPath = inputPath.replace('.csv', '_picked.csv')
        self.dataHandler.writeCsvData_arrDict(path=outputPath, arr=newArr)
        return outputPath

    def csv_removeRepeatByKey(self, inputPath='', outputPath='', key=''):
        if key=='':
            raise ValueError('key值为空，则无法去重。。请写入参数key的值')
        if outputPath == '':
            outputPath = inputPath.replace('.csv', '_removeRepeat.csv')
        arr = self.dataHandler.readCsvData_arrDict(inputPath)
        newArr = []
        for o in arr:
            sign = 0
            if key in o.keys()==False:
               raise ValueError('不存在该键值。'+key+"确保键值是正确的")
            for newa in newArr:
                if newa.get(key) == o.get(key):
                    sign = 1
            if sign == 0:
                newArr.append(o)
        self.dataHandler.writeCsvData_arrDict(path=outputPath, arr=newArr)
        return outputPath


if __name__ == '__main__':
    d = DataHandle()
    # # 处理数据，使得数据简化
    d.csv_execCode(inputPath='test.csv')
    # print("d1")
    # d.dataHandle(inputPath='handleDatas/test.csv', keys=['phone', 'message'],idkey='phone',outputPath='handleDatas/send.csv')
    # d.csv_addLine(inputPath='handleDatas/test_excCode_picked.csv',header='data',data=0)