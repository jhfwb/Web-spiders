import time
from _utils.RUtils import tool
from _xhr_tool.chromeRobot.src._decorator._decorator import chrome_robot_excute, chrome_datas_catch
from _xhr_tool.chromeRobot.src.domain.Action2 import Action
from _xhr_tool.chromeRobot.src.domain.ChromeFactory import ChromeFactory
from _xhr_tool.chromeRobot.src.domain.HighterAction2 import HigherAction
from _xhr_tool.chromeRobot.src.servlet.robot_thread import MyPipelineThread
from _xhr_tool.csv_tools._utils.CsvTool import CsvTool
from _xhr_tool.excuteEngine.Engine import ExcuteFuel
class Aaicaigou:
    key_word = '输送带'
    savePath='../datasStore/爱采购爬虫_'+key_word+'.csv'
    cycleTimes=-1
    saveCsvHeads=['公司名','联系人','电话','地址', '城市', 'qq', '微信','邮箱','_url']


    @chrome_robot_excute
    def web(self):
        Action().initWeb(url='https://www.11467.com/dir.html').\
            key_input(cssStr=".ivu-input", text=self.key_word, isClear=True). \
            click(cssStr=".search-btn"). \
            jumpBrowserTab(index=-1).excute()
    @chrome_robot_excute
    def webInit(self):#初始化
        def test(response):
            if response.datas=='':
                self.cycleTimes=1
            else:
                self.cycleTimes=int(response.datas)
        Action().scroll_browser_top_to_button(cssStr='.ivu-page-next',elemntName='下一页',timeOut=20).\
            find(cssStr='.ivu-page-item a',index=-1,after_func=test). \
            excuteBlock()
    @chrome_robot_excute
    def webRobot(self):
        def crapy(response):
            HigherAction().jumpBrowserTab(index=-1).\
            findCurrentUrl(key='_url', catchDate=True).\
            sendDatas(key_datas='公司名',datas=response.datas,catchDate=True).\
            find(cssStr='.nav-item').selcetAction(
                action1=HigherAction().click(cssStr='.nav-item:nth-child(4)',loadNewPage=True).jumpBrowserTab(index=-1).
                find(key='城市', cssStr='.icons',ignoreErr=False, catchDate=True).
                find(key='地址', cssStr='.section-container:nth-child(4)', catchDate=True).
                find(key='联系人', cssStr='.section-container:nth-child(2) .item-container .value',catchDate=True).
                find(key='电话', cssStr='.section-container:nth-child(2) .item-container:nth-child(2) .value',catchDate=True).
                find(key='邮箱', cssStr='.section-container:nth-child(2) .item-container:nth-child(3) .value',catchDate=True).
                find(key='qq', cssStr='.section-container:nth-child(2) .item-container:nth-child(4) .value',catchDate=True).
                find(key='微信', cssStr='.section-container:nth-child(2) .item-container:nth-child(5) .value',catchDate=True).
                sendDatas(key_datas='关键字',datas=self.key_word).closeCurrentBroswserTab()
            ).closeCurrentBroswserTab().excuteRightNow()
        for i in range(self.cycleTimes):
            crapyDatas=CsvTool().getCsvDatasByKey(path=self.savePath,isCreateFile=True,key='公司名')
            HigherAction().\
            click_all_except_crapyedDatas(cssStr='.p-card-desc-layout>div:last-child .name',func=crapy,crapyedDatas=crapyDatas).\
            click(cssStr='.ivu-page-next',ignoreErr=False).scroll_browser_top_to_button(cssStr='.ivu-page-next',elemntName='下一页',timeOut=60).excuteBlock()
            tool().print('...开始运行下一页...')
        print('运行结束')
    @chrome_datas_catch
    def dataSave(self,datas):
        # 1.将此数据保存到爬虫配置文件中。
        obj={}
        for saveCsvHead in self.saveCsvHeads:
            obj.setdefault(saveCsvHead,datas.get(saveCsvHead))
        print(obj)
        CsvTool().optionCsv(mode='a',path=self.savePath,datas=obj,isCreateFile=True)


if __name__ == '__main__':
    chromeFactory = ChromeFactory()
    chromeFactory.register(Aaicaigou)

