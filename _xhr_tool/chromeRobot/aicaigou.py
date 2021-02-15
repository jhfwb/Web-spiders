import time

from _xhr_tool.chromeRobot.src._decorator._decorator import chrome_robot_excute, chrome_datas_catch
from _xhr_tool.chromeRobot.src.domain.Action import Action
from _xhr_tool.chromeRobot.src.domain.ChromeFactory import ChromeFactory
from _xhr_tool.chromeRobot.src.domain.HighterAction import HigherAction
from _xhr_tool.chromeRobot.src.servlet.robot_thread import MyPipelineThread
from _xhr_tool.csv_tools._utils.CsvTool import CsvTool


class Aaicaigou:
    savePath='datasStore/爱采购爬虫.csv'

    @chrome_robot_excute
    def test(self):  # 初始化
        def t(response):
            print(response)
            return True
        HigherAction("爱采购").click_all(cssStr=".p-card-desc-layout>div:last-child .name",click_order='Sequential',before_click_func=t). \
            excute()


    # @chrome_robot_excute
    def webInit(self):#初始化
        Action("爱采购").initWeb(url='https://b2b.baidu.com/'). \
            key_input(cssStr=".ivu-input", text="吊装带", isClear=True). \
            click(cssStr=".search-btn").jumpBrowserTab(index=-1).\
            excute()
    # @chrome_robot_excute
    def webRobot(self):
        def crapy(response):
            # find(key='产品信息',cssStr='.rich-text.no-p-margin',catchDate=True). \
            Action().jumpBrowserTab(index=-1).find(key='公司名',cssStr='span.name',catchDate=True). \
                find(key='城市', cssStr='.address', catchDate=True,timeOut=3). \
                find(key='联系人',cssStr='.details-sections-item .item-container:nth-child(2) .value',catchDate=True).\
                find(key='手机',cssStr='.details-sections-item .item-container:nth-child(3) .value',catchDate=True).\
                find(key='电子邮箱',cssStr='.details-sections-item .item-container:nth-child(4) .value',catchDate=True).\
                find(key='详细地址',cssStr='.details-sections-item .item-container:nth-child(6) .value',catchDate=True).\
                sendDatas(key_datas='关键字',datas='吊装带',catchDate=True). \
                findCurrentUrl(key='_url',catchDate=True).\
                closeCurrentBroswserTab().\
                putActionToReadyAct(save=True)
        crapyDatas=CsvTool().getCsvDatasByKey(path=self.savePath,isCreateFile=True,key='公司名') #获取已爬虫数据
        HigherAction().scroll_browser_top_to_button().click_all_byName_differentName(cssStr='.p-card-desc-layout>div:last-child .name',func=crapy,crapyedDatas=
        crapyDatas).excute()
    # @chrome_datas_catch
    def dataSave(self,datas):
        # 1.将此数据保存到爬虫配置文件中。
        print(datas)
        # CsvTool().optionCsv(mode='a',path='datasStore/爱采购爬虫.csv',datas=datas,isCreateFile=True)
if __name__ == '__main__':
    chromeFactory = ChromeFactory()
    chromeFactory.register(Aaicaigou)

