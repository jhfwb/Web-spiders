from queue import Queue
from _xhr_tool._annotate import singleObj
from _xhr_tool._utils.pool.objsPool import ObjsPool
from _xhr_tool.chromeRobot.src.domain.ExcuteResponse import ExcuteResponse
@singleObj
class ExcuteResponsePool(ObjsPool):
    def __init__(self):
        super().__init__(obj_class=ExcuteResponse)
    def back(self, response:ExcuteResponse):
        super().back(response.initResponse())
    def get(self):
        return super().get()