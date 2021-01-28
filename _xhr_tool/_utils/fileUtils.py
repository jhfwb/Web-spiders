class FileUtils:
    def _getContextByPath(self, file='', encoding='utf-8'):
        fp = open(file=file, mode='r', encoding='utf-8')
        arr = fp.readlines()
        fp.close()
        pass