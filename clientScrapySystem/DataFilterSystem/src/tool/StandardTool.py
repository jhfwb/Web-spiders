from _xhr_tool._utils.CsvTool import CsvTool
class StandardTool:
    """
    标准化工具，由于爬取的客户资源不尽相同，因此需要将爬取的信息进行标准化处理。
    主要实现原理：
    通过template中的customerData_template.csv文件进行标准化指定

    """
    def __init__(self):
        self.csvTool = CsvTool()
        self.templateFilePath=''
    def makeStandard(self,datas=[]):
        """
        将datas数据标准化。根据csv中的数据
        """
        if len(datas)==0:
            return
        excel_standard_hands = self.csvTool.getHeader(path=self.templateFilePath+"template/customerData_template.csv")
        if not type(datas)==type([]):
            datas=[datas]
        ks=list(datas[0].keys())
        if not ks==excel_standard_hands:
            newdatas=[]
            for data in datas:
                newData = {}
                newHandArr=excel_standard_hands.copy()
                for i in range(len(newHandArr)):
                    newData.setdefault(newHandArr[i],None)
                keys=data.keys()
                for key in keys:
                    standardKey=self._change_standard_key_same(key,excel_standard_hands,newData)
                    if standardKey:
                        newData[standardKey]=data[key]
                for key in keys:
                    standardKey=self._change_standard_key(key,excel_standard_hands,newData)
                    if standardKey:
                        newData[standardKey]=data[key]
                newdatas.append(newData)
            return newdatas
        return datas
    def _change_standard_key_same(self, key, excel_standard_hands, data):

        for excel_standard_hand in excel_standard_hands:
            try:
                if data[excel_standard_hand] == None:
                    if excel_standard_hand == key:
                        return excel_standard_hand
            except:
                return None
        return ""
    def _change_standard_key(self,key,excel_standard_hands,data):

        for excel_standard_hand in excel_standard_hands:
            try:
                if data[excel_standard_hand]==None:
                    if excel_standard_hand in key:
                        return excel_standard_hand
            except:
                return None
        return ""