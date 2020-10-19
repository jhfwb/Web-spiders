import csv
class csvFileTool:
    """
    专门用来处理csv的工具。
    大大简化csv的交互
    """
    def __init__(self):
        pass
    def _check(self,path):
        pass
    def readCsvData_arrDict(self,path,encoding='utf-8'):
        """
        根据path读取csv文件。并以list的数组形式返回
        数组中的每一项都是字典的形式（dict）
        :param path:csv的路径
        :return:list数组，数组中每一项为字典
        """

        with open(path, 'r', encoding=encoding) as fp:
            # encoding是读取时候的解码规则
            readers = csv.DictReader(fp)
            return list(readers)
    def readCsvData_arrArr(self, path,encoding='utf-8'):
        """
        根据path读取csv文件。并以list的数组形式返回。
        数组中的每一项都是数组的形式

        :param path:csv的路径
        :return:list数组，数组中每一项为数组
        """
        with open(path, 'r', encoding=encoding) as fp:
            # encoding是读取时候的解码规则
            reader = csv.reader(fp)
            return list(reader)
    def writeCsvData_arrDict(self,path,arr,encoding='utf-8'):
        """
        以数组的形式写入。数组内部必须是字典形式
        :param path:
        :param arr:
        :return:
        """
        headers =list(arr[0].keys())
        with open(path, 'w', encoding=encoding,newline="") as fp:
            # encoding是读取时候的解码规则
            writer = csv.DictWriter(fp, headers)
            writer.writeheader()
            writer.writerows(arr)
    def writeData_arrArr(self, path,header=[], datas='',encoding='utf-8'):
        """
        :param path:  str | 保存的文件路径
        :param header: [] | 表格的表头
        :param datas:  [[],[],...] | 表格的数据
        :param encoding: str | 编码形式
        :return: None
        """
        with open(path, 'w', encoding=encoding, newline="") as fp:
            # encoding是读取时候的解码规则
            writer = csv.writer(fp)
            writer.writerow(header)
            writer.writerows(datas)