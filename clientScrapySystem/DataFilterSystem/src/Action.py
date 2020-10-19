from clientScrapySystem.DataFilterSystem.src.tool.DataCuter import DataCuter
from clientScrapySystem.DataFilterSystem.src.tool.DataLoad import DataHander
from clientScrapySystem.DataFilterSystem.src.tool.StandardTool import StandardTool


class Action:
    def __init__(self):
        # 获得数据处理工具
        dataHander=DataHander()
        # 载入数据。这里载入的数据已经写死。
        datasArr=dataHander.loadDatas()
        for i in range(0,len(datasArr)):
            # 将数据标准化
            datasArr[i]=StandardTool().makeStandard(datasArr[i])
            # 进入筛选器（不可用数据，目标可用数据，非目标可用数据）
            # 1.筛选关键词，
            # 2.筛选区域
            # 3.筛选
            dataCuter=DataCuter()
            datasKeys=dataCuter.dataCuterByKey(datasArr[i]) #根据关键词分割成元组，
            #datasKeys[0]# 目标
            #datasKeys[1]# 非目标客户。储存到垃圾箱文件中
            dataHander.saveDatas(fileNameSign='_丢弃',datas=datasKeys[1],fileName=dataHander.srcFilePaths[i])
            datasSites = dataCuter.dataCuterBySite(datasKeys[0])  # 根据低点分割成元组，
            dataHander.saveDatas(fileNameSign='_目标区域', datas=datasSites[0],fileName=dataHander.srcFilePaths[i])
            dataHander.saveDatas(fileNameSign='_非目标区域', datas=datasSites[1],fileName=dataHander.srcFilePaths[i])


