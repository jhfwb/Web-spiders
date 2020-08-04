import threading
import time
from queue import Queue

from selenium.webdriver.common.keys import Keys

from clientScrapySystem.chromeRobotSystem.Context import Context
from clientScrapySystem.chromeRobotSystem.domain.Action import Action
from utils.excelTool.ExcelTool import ExcelTool


class CCCF水带爬虫:
    #此处放入地址库
    def __init__(self):
        self.store=Queue()
        pass
    def run(self,myThread,company):
        self.start(myThread)
    def start(self,myThread):
        Action("客户定义"). \
            click(cssStr=".x-tool-maximize").\
            key_input(cssStr="input[id='ClientType.OPT']",text='其他').\
            select(cssStr="Select[name='Stype']",text='公司供应商'). \
            click(cssStr="input[name='ftype'][value='2']").\
            excute(myThread.readyExcute)


if __name__ == '__main__':
    con=Context()
    con.main()
    CCCF水带爬虫 = CCCF水带爬虫()
    #开启另外一个线程
    # threading.Thread(target=CCCF水带爬虫.data, args=[con]).start()
    CCCF水带爬虫.run(con.robotThread, "有衬里消防水带")




    #解决方案：
    #1.调成可以自己手动调整等待时间，这样每一步都能精准控制等待时间。
    #2.当出现超时等待的时候，并且该操作相对重要，这时候，就触发重新动作的机制。
    #3.设置不可忽略错误的动作。一旦该动作无法执行，只能重新启动，或者等待。