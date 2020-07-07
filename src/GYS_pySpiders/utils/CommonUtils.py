class CommonUtils:
    @staticmethod
    def changeStrToBool(s):
        if s=="True":
            return True
        else:
            return False

    @staticmethod
    def changeStrToList(str):
        """
        将字符串转成数组。如果字符串不是数组。则返回None。如果可以转换，则返回一个数组。
        """
        str=str.strip()
        if str.startswith('[') and str.endswith(']'):
            str = str[1:len(str) - 1].split(',')
            str = list(map(lambda x: x.strip().replace('\'', ''), str))
            return str
        return None
if __name__ == '__main__':
    a=CommonUtils.changeStrToList(" ['1', '2', 3 ]")
    print(a)