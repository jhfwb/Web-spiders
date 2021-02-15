from _xhr_tool._annotate import singleObj
from _xhr_tool._utils.RUtils import tool


@singleObj
class ActionControlInterpreter:
    """
    1. 解释Action的方法嵌套
    """
    def __init__(self):
        self.stack=[]
    def getControlState(self):
        return self.stack.pop()
    def judge(self,act):
        if act.get('way')=='connectLastBackFunction':
            return 'control'
        elif act.get('way')=='save':
            return 'save'
        else:
            return 'excute'
    def putControlState(self,act={},result=None):
        # print(act)
        # print(result)
        if act.get('_sign')=='connectLastBackFunction':#说明这个是Control语句
            self.stack.append(result)#将function的结尾放进去


