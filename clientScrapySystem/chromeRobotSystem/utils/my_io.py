#这个文件整合了所有与底层的所有io方法。
import csv
class MyIo:
    #读取文件,必须是csv的格式或者类格式.
    def read_file_csv(self,filepath="",encoding="ANSI"):
        arr=[]
        try:
            with open(filepath, "r", encoding="ANSI") as fp:
                reader=csv.DictReader(fp)
                arr=list(reader)
                fp.close()
                return arr
        except UnicodeDecodeError:
            with open(filepath, "r", encoding="utf-8") as fp:
                reader = csv.DictReader(fp)
                arr=list(reader)
                fp.close()
                return arr
        #对arr进行处理
