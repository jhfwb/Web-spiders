from _xhr_tool.csv_tools._utils.CsvTool import CsvTool
from _xhr_tool.csv_tools.csv_datas_filter.FILTER_KEY import FILTER_KEY


class DatasFilter:
    """
    1.过滤的key。2.过滤词。
    """

    def _filter_line(self,line='',filter_key=[]):
        for items in filter_key:
            if items in line:
                return True
        return False
    def filter_datas(self,datas=[],key="",encoding='utf-8',filter_key=[]):#1.滤词_选中，2.滤词_取出，3.未知数据
        """
        e.g.
        datas=[{'name':'张三',}]
        :param datas:
        :param key:
        :param encoding:
        :param filter_key: 一个数组。 当这个数据中的值在datas中都找不到时候，会被分到第二个数据
        :return: (,) 返回一个元组。第一个数据代表被选中的数据，第二个数据代表未被选中的数据
        """
        # datas=CsvTool().optionCsv(path=path,mode='r',encoding=encoding)
        filterArr=[]
        un_filterArr=[]
        for data in datas:
            if self._filter_line(line=data.get(key),filter_key=filter_key):
                filterArr.append(data)
            else:
                un_filterArr.append(data)
        return (filterArr,un_filterArr)
    def filter_csvFile(self,path,key,output_path_selected,ouput_path_unselected,encoding='utf-8',filterkey_arr=[]):
        datas = CsvTool().optionCsv(path=path, mode='r', encoding=encoding)
        datas=self.filter_datas(datas=datas,key=key,encoding=encoding,filter_key=filterkey_arr)
        CsvTool().optionCsv(datas=datas[0],path=output_path_selected, mode='w', encoding=encoding,isCreateFile=True)
        CsvTool().optionCsv(datas=datas[1],path=ouput_path_unselected, mode='w', encoding=encoding,isCreateFile=True)
        return datas
    pass
if __name__ == '__main__':
    # a=CsvTool().optionCsv(path='顺企网_key=吊装带.csv',mode='r')
    # print(a)
    # a=DatasFilter()._filter_line(line='河北省廊坊市固安县温泉休闲商务产业园区杨各庄村',filter_key=FILTER_KEY.selected)
    # print(a)
    a=DatasFilter().filter_csvFile(path="../顺企网_key=吊装带.csv",
                                   key='公司名',
                                   filterkey_arr=FILTER_KEY.selected,
                                   output_path_selected='../test/输出.csv',
                                   ouput_path_unselected='../test/输出未选中.csv'
                                   )
    print(a)