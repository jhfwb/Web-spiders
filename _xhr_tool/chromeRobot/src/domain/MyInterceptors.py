import time
import logging
from _xhr_tool._utils.RUtils import tool
from _xhr_tool.chromeRobot.src._chromeRobot_tool.decoratorUtils import DecoratorEngine
from _xhr_tool.chromeRobot.src._chromeRobot_tool.excuteResponsePool import ExcuteResponsePool

from _xhr_tool.chromeRobot.src.domain.ExcuteResponse import ExcuteResponse
from _xhr_tool.excuteEngine.Component import ExcuteInterceptor, BackFuelInterceptor
from _xhr_tool.excuteEngine.Engine import ExcuteFuel
#自定义打断器————————请在ChromeFactory.class中注册打断器
#保存爬虫对象
class SaveFindDatas(ExcuteInterceptor):# 保存find方法的。
    """
    保存输出的数据。当出现异常的时候，则
    """
    def __init__(self):
        from _xhr_tool.chromeRobot.src.domain.ChromeFactory import ChromeFactory
        self.saveObj={}
        self.chromeFactory=ChromeFactory()
    def intercept_before_excute(self, fuel:ExcuteFuel):
        pass
    def intercept_after_excute(self, fuel:ExcuteFuel):
        # 导入模块
        if fuel.get_meta().get('act')=='save':
            if self.saveObj!={}:
                if fuel.get_meta().get('err') != None and fuel.get_meta().get('err') == True:
                    # 错误打印出来：
                    tool().print('保存错误:该页面爬取失败:' +str(self.saveObj))#!!!xhr建议此处保存在错误日记中
                else:
                    DecoratorEngine().excuteDecorator(obj=self.chromeFactory.user,decoratorName='@chrome_datas_catch',args=[self.saveObj])
            self.saveObj={}
        if fuel.get_meta().get('catchDate') != None:
            if fuel.get_meta().get('catchDate'):
                if fuel.get_func_result().key_datas!=None or fuel.get_func_result().datas!=None:
                    self.saveObj.setdefault(fuel.get_func_result().key_datas,fuel.get_func_result().datas)
class BackResponse(BackFuelInterceptor):
    """
    负责回收response对象。此打断器必须最后执行，否则此前的打断器会出现异常
    """
    def intercept_before_backFuel(self, fuel):
        # 导入模块
        if fuel.get_func_result()!=None:
            ExcuteResponsePool().back(fuel.get_func_result())
        pass
    def intercept_after_backFuel(self, fuel):
        # 导入模块
        pass

#执行计时器,为了避免频繁访问。插入此方法，控制访问频率
class ExcuteInterval(ExcuteInterceptor):# 保存find方法的。
    func_names=['click_element_apparent','get_url']
    def intercept_before_excute(self, fuel:ExcuteFuel):
        pass
    def intercept_after_excute(self, fuel:ExcuteFuel):
        if fuel.get_func()!=None:
            if fuel.get_func().__name__ in self.func_names:
                time.sleep(5)#等待5秒钟
class ActionIterceptor(ExcuteInterceptor):# 保存find方法的。
    """
    确保动作的连续性，当该动作失败的时候，不会再执行后面的动作,并且会将通知后续save打断器
    """
    unexcuteIds = []
    def intercept_before_excute(self, fuel:ExcuteFuel):
        for unexcuteId in self.unexcuteIds:
            if unexcuteId==fuel.get_meta().get('id'):
                if fuel.get_meta().get('act')=='save':
                    fuel.get_meta().setdefault('err',True)
                else:
                    fuel.setFuel()#将次方法重置.重置之后，则不会再执行该方法
    def intercept_after_excute(self, fuel:ExcuteFuel):
        response=fuel.get_func_result()
        if fuel.get_meta().get('ignoreErr')==True:
            pass
        elif fuel.get_meta().get('ignoreErr')==False:
            if response!=None and response.success==False:#当该动作执行失败的时候,则通知后续相关动作，不再执行
                self.unexcuteIds.append(fuel.get_meta().get('id'))