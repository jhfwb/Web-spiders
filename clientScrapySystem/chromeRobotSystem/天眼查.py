import time
from queue import Queue

from selenium.webdriver.common.keys import Keys
from clientScrapySystem.chromeRobotSystem.Context import Context
from clientScrapySystem.chromeRobotSystem.domain.Action import Action
class 天眼查:
    #此处放入地址库
    def __init__(self):
        self.store=Queue()
        pass
    def run(self,myThread,company):
        def monitor(driver):
            #判断是否是机器人，如果是则开启闹钟。如果不是则继续执行
            if "我们只是确认一下你不是机器人" in driver.page_source:#碰到检验了。这时候会发出声音让你帮忙检验
                while True:
                    time.sleep(5)
                    print("请验证验证码!!!!")
                    if "我们只是确认一下你不是机器人" not in driver.page_source:
                        break
        def exception(action):
            action.find(cssStr="div.in-block.sup-ie-company-header-child-1 > span:nth-child(2)", key="手机",timeOut=5)
        def success(action):
            action.find(cssStr=".phone-item .phone", key="手机", mode="multiple",timeOut=5).\
            click(cssStr=".modal-dialog .close")
        Action("天眼查搜寻公司信息").initWeb().\
            get("https://www.tianyancha.com/?jsid=SEM-BAIDU-PZ2006-SY-000001").\
            key_input(cssStr="[type='search']",text=company,isClear=True,timeOut=5,errProcessCase="combine").\
            key_input(cssStr="[type='search']",text=Keys.ENTER,isClear=False,timeOut=5,errProcessCase="combine").\
            click(cssStr="div.result-list.sv-search-container > div:nth-child(1) a.name",timeOut=5,errProcessCase="clear_action",monitor=monitor). \
            find(cssStr=".name",key="公司名",timeOut=5,errProcessCase="combine").\
            find(cssStr=".name>.link-click", key="客户"). \
            find(cssStr=".auto-folder", key="地址"). \
            find(cssStr="tbody > tr:nth-child(11) > td:nth-child(2) > span", key="产品"). \
            find(cssStr=".summary", key="信息"). \
            find(cssStr=".-breakall > tbody > tr:nth-child(1) > td:nth-child(4)", key="资本"). \
            find(cssStr=".-breakall  tr:nth-child(5) > td:nth-child(4)", key="模式"). \
            get_current_url(key="_url2"). \
            find(cssStr=".tag-list", key="经营状况"). \
            click(cssStr="span.link-click.link-spacing",exception=exception,success=success,timeOut=2).\
            excute(myThread.readyExcute)
if __name__ == '__main__':
    con=Context()
    con.main()
    天眼查 = 天眼查()
    天眼查.run(con.robotThread, "fewfewljfewlkje")
    items = con.robotThread.itemsQueue.get()  # 爬取的信息
    print(items)

    #解决方案：
    #1.调成可以自己手动调整等待时间，这样每一步都能精准控制等待时间。
    #2.当出现超时等待的时候，并且该操作相对重要，这时候，就触发重新动作的机制。
    #3.设置不可忽略错误的动作。一旦该动作无法执行，只能重新启动，或者等待。