from queue import Queue

from _xhr_tool._annotate import singleObj
from _xhr_tool.chromeRobot.src.domain.ChromeFactory import ChromeFactory
@singleObj
class ResponseHandler:
    items={}
    actions=Queue(10)
    def handle(self,response):
        if response.datas != None:
            if response.option.get("catchDate"):
                self.items.setdefault(response.key_datas,response.datas)
    def sendItems(self):
        if self.items!={}:
            items = ChromeFactory().getPassageway().put(self.items)
        self.items={}
        pass
# if __name__ == '__main__':
