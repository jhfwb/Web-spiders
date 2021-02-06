from _xhr_tool.csv_tools._utils.CsvTool import CsvTool


class CsvDataRemoveRepeat:
    """
    csv内部数据处理工具
    1.去重
    """
    def _removeRepeatByKey(self,key,datas):
        """
        根据key值，去除掉重复的数据
        e.g:
            >>>datas=[{'1':'哈哈'},{'1':'哈哈'},{'1':'嘻嘻'},{'1':'嘻嘻2'},{'1':'哈哈'}]
            >>>datas=CsvDataRemoveRepeat()._removeRepeatByKey(key='1',datas=datas)
            >>>print(datas) ##输出[{'1': '哈哈'}, {'1': '嘻嘻2'}, {'1': '嘻嘻'}]
        :param key:
        :param datas:数据集，必须是[{}, {}, {}]的形式
        :return:
        """
        arr=[]
        for i in range(len(datas)):
            sign=1
            data=datas.pop()
            for next in arr:
                if data.get(key)==next.get(key):
                    sign=0
            if sign==1:
                arr.append(data)
        return arr
            # arr.append(data)
    def csvRemoveRepeatByKey(self,key,path='',encoding='utf-8'):
        """
        根据key值，去除掉掉文件中重复的数据
        e.g:
            >>>datas=CsvDataHandler().csvRemoveRepeatByKey(key='公司名称',path='../../chromeRobot/datasStore/水带厂家.csv')
        :param key:
        :param path:
        :param encoding:
        :return:
        """
        datas=self._removeRepeatByKey(key=key,datas=CsvTool().optionCsv(path=path,encoding=encoding,mode='r'))
        CsvTool().optionCsv(path=path, encoding=encoding, mode='w',datas=datas)



if __name__ == '__main__':
    datas=[{'1':'哈哈'},{'1':'哈哈'},{'1':'嘻嘻'},{'1':'嘻嘻2'},{'1':'哈哈'}]
    CsvDataHandler().csvRemoveRepeatByKey(key='公司名称', path='../../chromeRobot/datasStore/水带厂家.csv')