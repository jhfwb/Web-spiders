from _xhr_tool.chromeRobot.src.domain.Action import Action


class HigherAction(Action):
    def __init__(self,memo="请输入备注信息",callBackFunc=lambda x:x):
        super().__init__(memo="请输入备注信息",callBackFunc=lambda x:x)
    def thinking_click(self,cssStr="",func=lambda x:x,func_args=[],sign='',index=0):
        # 泰州市东升吊装设备有限公司
        def _back1(response,sign,cssStr,func,func_args,index):
            if response.datas==sign:
                Action().click(cssStr=cssStr,index=index,func=func,func_args=func_args).putActionToReadyAct()
            else:
                print('不匹配:sign为:'+sign+'; 实际数据为:'+response.datas)
                return False
        self.find(cssStr=cssStr,index=index,mode='single',catchDate=False,func=_back1,func_args=[sign,cssStr,func,func_args,index]) #存让发
        # self.connectLastBackFunction(func=_back2)
        return self
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
                action1.putActionToReadyAct()
            else:
                action2.putActionToReadyAct()
        self.connectLastBackFunction(func=_select)
        return self
if __name__ == '__main__':
    HigherAction().thinking_click(cssStr='.p-card-desc-layout>div:last-child .name',sign='泰州市东升吊装设备有限公司').excute()