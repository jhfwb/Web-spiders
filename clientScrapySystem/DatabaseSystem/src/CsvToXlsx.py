from _xhr_tool._utils.excelTool.ExcelTool import ExcelTool
import shutil, os

class CsvToXlsx:
    def __init__(self):
        self.tool= ExcelTool()
        self.dirPath='../database/smelter/'
        self.garbagePath='../database/garbage'
        pass
    def changeCsvToXlsx(self,path=''):
        self.tool.chageCsvToExcelFile(path, encoding='ANSI')
        pass
    def working(self):
        """
        主要任务：负责将smelter文件夹中的csv文件转化成xlsx文件。并把原本的csv文件转移到garbage中。
        """
        needsChanges=[]
        for root, dirs, files in os.walk(self.dirPath):
            for file in files:
                if file!='readme.txt':
                    if file.endswith('.csv'):
                        needsChanges.append(self.dirPath+file)
        if len(needsChanges)==0:
            return False
        for needsChange in needsChanges:
            self.tool.chageCsvToExcelFile(path=needsChange,encoding='ANSI')
            shutil.move(needsChange,self.garbagePath)
        return True
    def working2(self):
        """
        主要任务：负责将smelter文件夹中的xlsx文件转化成csv文件。并把原本的csv文件转移到garbage中。
        """
        needsChanges = []
        for root, dirs, files in os.walk(self.dirPath):
            for file in files:
                if file != 'readme.txt':
                    if file.endswith('.xlsx'):
                        needsChanges.append(self.dirPath + file)
        if len(needsChanges) == 0:
            return False
        print(needsChanges)
        for needsChange in needsChanges:
            self.tool.changeExeclToCsvFile(path=needsChange)
            shutil.move(needsChange, self.garbagePath)
        return True
if __name__ == '__main__':
    CsvToXlsx().working()
