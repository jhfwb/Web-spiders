"""
用于处理与文件的关系。
"""

class FileUtils:
    def _getContextByPath(self, file='', encoding='utf-8'):
        fp = open(file=file, mode='r', encoding='utf-8')
        arr = fp.readlines()
        fp.close()
        pass
class TxtTool:
    """"""
    def readDatas(self,path='',encoding='utf-8'):
        fp = open(file=path, mode='r', encoding=encoding,)
        arr = fp.readlines()
        fp.close()
        arr=list(map(lambda x:x.strip(),arr))
        return arr
if __name__ == '__main__':
    arr=TxtTool().readDatas(path='客户信息.txt')
    print(arr)