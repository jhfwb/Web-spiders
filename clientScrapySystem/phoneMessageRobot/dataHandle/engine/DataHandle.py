import os
import re as re1
import shutil
from _utils.CsvTool import CsvTool
from _utils.RUtils import tool
from _utils.excelTool.csvFileOptionTool import csvFileTool
from pathlib import Path
from clientScrapySystem.phoneMessageRobot.dataHandle.engine import DiskFilePath, DiskDirPath
class DataHandle:
    """
    用于处理数据
    """
    re_2 = re1.compile(r'\{\{(.*)\}\}')
    """匹配{{}}中的内容的正则表达式"""
    re_3 = re1.compile(r'\(\(re=(.*)\)\)')
    """匹配(())中的内容的正则表达式"""
    re_4 = re1.compile(r'.*\{\{.*\}\}$')
    """匹配{{}}并以}为结尾的字符串"""
    def __init__(self):
        self.dataHandler = csvFileTool()
        pass
    def dataHandle(self,filePath=''):
        """
        处理filePath对应的文件，主要执行以下几个流程:
        1.复制源文件到disk/src_datas中
        2.对源文件进行代码执行，执行成功的
        """
        if not os.path.exists(filePath):
            raise FileNotFoundError('未找到该文件:'+filePath+'。请确保该文件存在!')
        fileName=os.path.basename(filePath)
        # 创建filePath源文件，并保存在指定文件夹。
        try:
            shutil.copy(filePath,DiskDirPath.src_datas)
        except shutil.SameFileError:
            pass
        # 1.生成执行文件,并将执行文件存入到disk/excute_datas/文件夹中。将执行失败的文件存入到disk/excute_datas_err文件中。
        self.csv_execCode(inputPath=Path(DiskDirPath.src_datas).joinpath(fileName),outputPath=
        Path(DiskDirPath.excute_datas).joinpath(fileName.replace('.csv','_exc.csv')),err_outputPath=
        Path(DiskDirPath.excute_datas_err).joinpath(fileName.replace('.csv','_exc_err.csv')))
        # 2.取出已发送的电话号码，放入disk/sendedData文件中共
        sendedPhones=list(map(lambda x:x.get('phone'),CsvTool().optionCsv(path=DiskFilePath.sended_datas,mode='r')))
        # 3.将disk/excute_datas中的数据一条条输入到disk/readySendData/文件中，以disk/sendedData中电话号码为key值，
        excute_datas = CsvTool().optionCsv(path= Path(DiskDirPath.excute_datas).joinpath(fileName.replace('.csv','_exc.csv')), mode='r') #待发送的数据
        ready_send_datas = list(CsvTool().optionCsv(path=DiskFilePath.ready_send_datas, mode='r',isCreateFile=True))
        mid_ready_send_datas=[]
        for excute_data in excute_datas:
            if not excute_data['phone'] in sendedPhones:
                # ready_send_datas.append({'phone',excute_data['phone']})
                mid_ready_send_datas.append(excute_data)
        for mid_ready_send_data in mid_ready_send_datas:
            if mid_ready_send_data.get('phone') not in map(lambda x:x.get('phone'),ready_send_datas):
                ready_send_datas.append(mid_ready_send_data)
        CsvTool().optionCsv(path=DiskFilePath.ready_send_datas, mode='w',datas=ready_send_datas)
        # print(ready_send_datas)
        # 以及disk/readySendData中的值，一条条去除掉已经发送过的电话号码

        # return self.dataHandler.readCsvData_arrDict(outputPath)

    def csv_addLine(self,inputPath='',outputPath='',header="",data=""):
        dics=self.dataHandler.readCsvData_arrDict(inputPath)
        # dic=list(map(lambda x:x.setdefault(header,data); return x;,dic))
        for i in range(len(dics)):
            dics[i].setdefault(header,data)
        if outputPath=="":
            outputPath=inputPath.replace('.csv','_add'+header+'.csv')
        self.dataHandler.writeCsvData_arrDict(path=outputPath,arr=dics)
        return outputPath
    def _check_grammar(self,line):
        """
        检查语法格式，需要满足
        XX{{XX}}((XX))
        XX{{XX}}
        两种形式
        """
        if re1.match(re1.compile(self.re_4),line):
            return True
        if line.endswith('))') and "}}((" in line:
            return True
        return False
    def csv_execCode(self, inputPath='', outputPath='',err_outputPath=''):
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
        inputPath=str(inputPath)
        outputPath = str(outputPath)
        err_outputPath = str(err_outputPath)
        if inputPath.endswith('.csv') == False:
            raise NameError('请确保传入的inputPath是csv文件~~~୧(๑•̀◡•́๑)૭')
        # 获得原始数据的数组
        srcDatas = self.dataHandler.readCsvData_arrArr(inputPath) #srcDatas-从inputPath文档中获得的内存数据。是一个集合
        header = [] # header-新数据的表头
        headerHandles = [] # headerHandles-存放执行代码
        removeHeader=[]
        # 为header与headerHandles存入其值。
        for i in range(0, len(srcDatas[0])):
            srcDatas[0][i]=self._removeStrip(srcDatas[0][i])
            # print(srcDatas[0][i])
            if self._check_grammar(srcDatas[0][i])==False:  # 对语法头进行语法检查。
                raise SyntaxError('csv中表头语法格式错误:'+str(srcDatas[0][i])+'。请确保如下格式:表头名称{{语法}}((正则表达式))')
            reArr = re1.findall(self.re_2, srcDatas[0][i])
            reCheckArr = re1.findall(self.re_3, srcDatas[0][i])
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
            datas.append(arr)
        headerHandles = list(map(lambda x: (x[1], x[2]), headerHandles)) # 保存执行语句
        datasErro = []
        locVab={} #本地变量 用于储存exe中的返回值。
        locEnv={} #本地环境 将一个作用域表示成一个对象。
        for index in range(0, len(datas)):  # 遍历所有datas  | datas=[['许焕燃', '13805980379', ''],['许焕燃', '13805980379', '']]
            for j in range(0, len(datas[index])): #  遍历datas中的每一项 |  data[j]=['许焕燃', '13805980379', '']
                de = headerHandles[j][0].split('=')[0] #  de:
                # tool.print(datas[index][j],fontColor='yellow')
                a = None
                if headerHandles[j][1] != '':
                    a = re1.fullmatch(headerHandles[j][1], datas[index][j])
                else:
                    a = ""
                if a == None:
                    datasErro.append(srcDatas[index+1]) #
                    datas[index] = None
                    break
                if de.startswith('!'):
                    de=de[1:]
                exec(de + '="' + datas[index][j] + "\"",locEnv,locVab)
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
        if err_outputPath=="":
            err_outputPath=inputPath.replace('.csv', '_excCode_err.csv')
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
        for i in range(len(datas)):
            for remove in removeId:
                del datas[i][remove]
        self.dataHandler.writeData_arrArr(outputPath, header=header, datas=datas)
        self.dataHandler.writeData_arrArr(err_outputPath, header=srcDatas[0], datas=datasErro)
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

    def _removeStrip(self, line):
        line=line.strip()
        li1=re1.findall(self.re_2,line)
        li2=re1.findall(self.re_3,line)
        if len(li1)!=0:
            line=line.replace(li1[0],li1[0].strip())
        if len(li2)!=0:
            line=line.replace(li2[0],li2[0].strip())
        return line

if __name__ == '__main__':
    pass
    d = DataHandle()
    # # 处理数据，使得数据简化
    d.dataHandle(filePath='../disk/src_datas/test_.csv')
    # print("d1")
    # d.dataHandle(inputPath='handleDatas/test.csv', keys=['phone', 'message'],idkey='phone',outputPath='handleDatas/send.csv')
    # d.csv_addLine(inputPath='handleDatas/test_excCode_picked.csv',header='data',data=0)