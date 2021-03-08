import random

from _xhr_tool.chromeRobot.src.domain.Action import Action


class HigherAction(Action):
    def __init__(self,memo="请输入备注信息",callBackFunc=lambda x:x):
        super().__init__(memo="请输入备注信息",callBackFunc=lambda x:x)

    def find(self,cssStr="",key="请为key赋值",mode="single" or "multiple",index=0,func=lambda x:x,catchDate=True,func_args=[],timeOut=3):

        self.find(cssStr=cssStr,key=key,mode=mode,index=index,func=func,func_args=func_args,timeOut=timeOut)
    def click_all(self, cssStr="",before_click_func=lambda x:True,before_click_func_args=[], func=lambda x: x, func_args=[], click_order='random' or 'sequential'):
        """
        点击所有被选中的选择器。在每次点击完毕后，会执行回调方法。点击的时候会默认打乱顺序。
        :param cssStr: 选择器（可以选择多个）
        :param func: 回调函数
        :param func_args: 回调函数的参数
        :param click_order: 点击顺序。random：随机点击(默认)。sequential：顺序点击。
        :return:
        """
        def _data(response):
            datas = response.datas
            _action = HigherAction()
            for i in range(len(datas)):
                if before_click_func({'click_name':datas[i],'all_click_names':datas,'click_index':i},*before_click_func_args)==True:
                    _action.click(cssStr=cssStr, func_args=func_args, func=func, index=i)
            if click_order == 'random':
                _action._randomBufferActs().putActionToReadyAct(immediately=False)
            elif click_order == 'Sequential':
                _action.putActionToReadyAct(immediately=False)
            else:
                raise ValueError('click_orderd的值：' + click_order + '出现错误，只允许是random(随机的)或者Sequential(顺序的);')

        # 1.找到所有数据。
        self.find(cssStr=cssStr, mode='multiple', func=_data, catchDate=False)
        return self
    def click_all2(self,cssStr="",func=lambda x:x,func_args=[],click_order='random' or 'sequential'):
        """
        点击所有被选中的选择器。在每次点击完毕后，会执行回调方法。点击的时候会默认打乱顺序。
        :param cssStr: 选择器（可以选择多个）
        :param func: 回调函数
        :param func_args: 回调函数的参数
        :param click_order: 点击顺序。random：随机点击(默认)。sequential：顺序点击。
        :return:
        """
        def _data(response):
            datas=response.datas
            _action=HigherAction()
            for i in range(len(datas)):
                _action.click(cssStr=cssStr,func_args=func_args,func=func,index=i)

            if click_order=='random':
                _action._randomBufferActs().putActionToReadyAct(immediately=False)
            elif click_order=='Sequential':
                _action.putActionToReadyAct(immediately=False)
            else:
                raise ValueError('click_orderd的值：'+click_order+'出现错误，只允许是random(随机的)或者Sequential(顺序的);')
        # 1.找到所有数据。
        self.find(cssStr=cssStr, mode='multiple',func=_data,catchDate=False)
        return self


    def click_all_byName_differentName(self,cssStr="",crapyedDatas=[],func=lambda x:x,func_args=[]):
        """
        点击所有cssStr下的元素。
        1.已经被点击过的，名字相同的元素不会点击。
        2.crapyedDatas中的数据不会被点击
        其中crapyedDatas代表已经爬虫过的数据。这些数据是不被点击的。
        :param cssStr:
        :param crapyedDatas:
        :param func:
        :param func_args:
        :return:
        """
        def _data(response,crapyedDatas):
            datas=response.datas
            _action=HigherAction()
            clicked_names=[] #已经点过的数据也不会再点
            for i in range(len(datas)):
                if datas[i] not in crapyedDatas and datas[i] not in clicked_names:
                    clicked_names.append(datas[i])
                    _action.click(cssStr=cssStr,func_args=func_args,func=func,index=i)
            _action._randomBufferActs().putActionToReadyAct(immediately=False)
        # 1.找到所有数据。
        self.find(cssStr=cssStr, mode='multiple',func=_data,func_args=[crapyedDatas],catchDate=False)
        # 2.比对数据
        return self
    def click_all_byName(self,cssStr="",crapyedDatas=[],func=lambda x:x,func_args=[]):
        """
        点击所有cssStr下的元素。
        1.已经被点击过的，名字相同的元素不会点击。
        2.crapyedDatas中的数据不会被点击
        其中crapyedDatas代表已经爬虫过的数据。这些数据是不被点击的。
        :param cssStr:
        :param crapyedDatas:
        :param func:
        :param func_args:
        :return:
        """
        def _data(response,crapyedDatas):
            datas=response.datas
            _action=HigherAction()
            for i in range(len(datas)):
                if datas[i] not in crapyedDatas :
                    _action.click(cssStr=cssStr,func_args=func_args,func=func,index=i)
            _action._randomBufferActs().putActionToReadyAct(immediately=False)
        # 1.找到所有数据。
        self.find(cssStr=cssStr, mode='multiple',func=_data,func_args=[crapyedDatas],catchDate=False)
        # 2.比对数据
        return self
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
    def _randomBufferActs(self):
        """
        打乱执行顺序
        :return:
        """
        random.shuffle(self._bufferActs)
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
    pass
    # HigherAction().thinking_click(cssStr='.p-card-desc-layout>div:last-child .name',sign='泰州市东升吊装设备有限公司').excute()