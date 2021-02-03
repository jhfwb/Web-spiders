from _xhr_tool._utils.RUtils import tool
from _xhr_tool.chromeRobot.domain.Action import Action
from _xhr_tool.chromeRobot.domain.ExcuteResponse import ExcuteResponse
class HigherAction(Action):
    def __init__(self,memo="请输入备注信息",callBackFunc=lambda x:x):
        super().__init__(memo="请输入备注信息",callBackFunc=lambda x:x)
    def selcetAction(self,action1,action2):
        """
        action1与action2
        :param action1:
        :param action2:
        :return:
        """
        if action1==self:
            raise ValueError("该参数action1指向的对象不允许是调用该方法的对象:请传入一个新创建Action")
        if action1==self:
            raise ValueError("该参数action2指向的对象不允许是调用该方法的对象:请传入一个新创建Action")
        def _select(result):
            if result:
                action1.excuteActionRightNow()
            else:
                action2.excuteActionRightNow()
        self.connectLastBackFunction(func=_select)
        return self
if __name__ == '__main__':
    pass