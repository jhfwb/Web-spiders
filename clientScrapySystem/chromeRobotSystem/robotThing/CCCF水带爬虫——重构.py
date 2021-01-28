import threading
import time
from queue import Queue

from clientScrapySystem.chromeRobotSystem.Context import Context
from clientScrapySystem.chromeRobotSystem.domain.Action import Action
from _xhr_tool._utils.excelTool.ExcelTool import ExcelTool
from clientScrapySystem.chromeRobotSystem.domain.ChromeFactory import ChromeFactory


class CCCF水带爬虫:
    #此处放入地址库
    # def __init__(self):
    #     self.store=Queue()
    #     pass
    # def run(self,myThread):
    #     self.start(myThread)
    #     while range(262):
    #         self.cycleRun(myThread)
    #         time.sleep(2)
    def cycleRun(self):
        Action("天眼查搜 寻公司信息").\
        find(cssStr="td[valign='top'] tbody tr:nth-child(2) table td>div>div:nth-child(3)>div:nth-child(2)", key="产品型号",mode='multiple'). \
        find(cssStr="td[valign='top'] tbody tr:nth-child(2) table td>div>div:nth-child(3)>div:nth-child(4)", key="公司名称",mode='multiple'). \
        find(cssStr="td[valign='top'] tbody tr:nth-child(2) table td:nth-child(5) span", key="准入状态",mode='multiple'). \
            click(cssStr="td[align='right'] a:nth-child(3)", timeOut=5,
                  errProcessCase="clear_action").\
            excute()\

        pass
    def start(self,myThread):
        Action("天眼查搜寻公司信息").initWeb(). \
            get("http://www.cccf.com.cn/certSearch/"). \
            key_input(cssStr="input[name=productName]", text="有衬里消防水带", isClear=True, timeOut=5,
                      errProcessCase="combine"). \
            click(cssStr="input[type='submit']", timeOut=5,
                  errProcessCase="clear_action").click(cssStr="td[align='right'] a:nth-child(2)", timeOut=5,
                  errProcessCase="clear_action").\
            excute(myThread.readyExcute)
    def data(self,con):
        print('开始数据采集')
        excel=ExcelTool()
        while True:
            items = con.robotThread.itemsQueue.get()  # 爬取的信息
            if items=='异常终止ACTION':
                continue
            datas=[]
            try:
                datas = excel.optionExecl(path='消防水带厂家.xlsx', mode='r')
            except IndexError and FileNotFoundError:
                excel.optionExecl(path='消防水带厂家.xlsx', datas=[], mode='w')
            产品型号s = items['产品型号']
            公司名称s = items['公司名称']
            准入状态s = items['准入状态']
            itemss = []
            for i in range(len(产品型号s)):
                item = {'公司名称': 公司名称s[i], '产品型号': 产品型号s[i], '准入状态': 准入状态s[i]}
                itemss.append(item)
            excel.optionExecl(path='消防水带厂家.xlsx', datas=itemss, mode='a')
if __name__ == '__main__':
    chromeFactory=ChromeFactory()
    print('?')
    print(type(CCCF水带爬虫))
    chromeFactory.register(CCCF水带爬虫)
    chromeFactory.run(CCCF水带爬虫.cycleRun)
    # threading.Thread(target=CCCF水带爬虫.data, args=[con]).start()
    # CCCF水带爬虫.run(con.robotThread, "有衬里消防水带")




    #解决方案：
    #1.调成可以自己手动调整等待时间，这样每一步都能精准控制等待时间。
    #2.当出现超时等待的时候，并且该操作相对重要，这时候，就触发重新动作的机制。
    #3.设置不可忽略错误的动作。一旦该动作无法执行，只能重新启动，或者等待。