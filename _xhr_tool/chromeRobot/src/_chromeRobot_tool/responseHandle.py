from queue import Queue

from _xhr_tool._annotate import singleObj
from _xhr_tool.chromeRobot.src.domain.ChromeFactory import ChromeFactory
@singleObj
class ResponseHandler:
    items={}
    actions=Queue(10)
    def getItems(self):
        return self.items
    def handle(self,response):
        if response.option.get("catchDate"):
            if response.datas != None:
                self.items.setdefault(response.key_datas,response.datas)
            else:
                self.items.setdefault(response.option.get('key'),'未找到该数据')
    def sendItems(self):
        if self.items!={}:
            items = ChromeFactory().getPassageway().put(self.items)
        self.items={}
        pass
# if __name__ == '__main__':
