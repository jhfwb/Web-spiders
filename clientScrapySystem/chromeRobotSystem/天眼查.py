from queue import Queue

from selenium.webdriver.common.keys import Keys
from clientScrapySystem.chromeRobotSystem.domain.Action import Action


class 天眼查:
    #此处放入地址库
    def __init__(self):
        self.store=Queue()
        pass
    def run(self,myThread,company):
        def exception(action):
            action.find(cssStr="div.f0 span:nth-child(2)", key="手机")
        def success(action):
            action.find(cssStr=".phone-item .phone", key="手机", mode="multiple").\
            click(cssStr=".modal-dialog .close")
        Action("天眼查搜寻公司信息").initWeb().\
            get("https://www.tianyancha.com/?jsid=SEM-BAIDU-PZ2006-SY-000001").\
            key_input(cssStr="[type='search']",text=company,isClear=True).\
            key_input(cssStr="[type='search']",text=Keys.ENTER,isClear=False).\
            click(cssStr="div.result-list.sv-search-container > div:nth-child(1) a.name").\
            find(cssStr=".name",key="公司名").\
            find(cssStr=".name>.link-click", key="客户"). \
            find(cssStr=".auto-folder", key="地址"). \
            find(cssStr="tbody > tr:nth-child(11) > td:nth-child(2) > span", key="产品"). \
            find(cssStr=".summary", key="信息"). \
            find(cssStr=".-breakall > tbody > tr:nth-child(1) > td:nth-child(4)", key="资本"). \
            find(cssStr=".-breakall  tr:nth-child(5) > td:nth-child(4)", key="模式"). \
            get_current_url(key="_url2"). \
            find(cssStr=".tag-list", key="经营状况"). \
            click(cssStr="span.link-click.link-spacing",exception=exception,success=success).\
            excute(myThread.readyExcute)