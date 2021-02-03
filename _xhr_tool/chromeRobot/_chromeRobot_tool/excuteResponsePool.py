from queue import Queue
from _xhr_tool._annotate import singleObj
from _xhr_tool.chromeRobot.domain.ExcuteResponse import ExcuteResponse
@singleObj
class ExcuteResponsePool:
    def __init__(self,responseNum=5):
        self.pool=Queue()
        for i in range(responseNum):
            self.pool.put(ExcuteResponse())
    def getResponse(self):
        #type: () -> ExcuteResponse
        response:ExcuteResponse= self.pool.get()
        response.initResponse()
        return response
    def backResponse(self,response):
        self.pool.put(response)