import uuid
from queue import Queue

from clientScrapySystem.chromeRobotSystem.domain.Action import Action


class ActionLink:
    def __init__(self,arr):
        self.actions=Queue()
        self._id=str(uuid.uuid1())
        pass

    def getActioins(self):
        return self.actions

    def createAction(self):
        action=Action()
        action._id=str(uuid.uuid1())
        self.actions.put(action)
        return action