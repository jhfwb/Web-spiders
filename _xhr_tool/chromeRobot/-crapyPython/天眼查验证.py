from _xhr_tool._utils import relpath
from _xhr_tool._utils.arr_caculate import remove_repeat_arr_inner_dict
from _xhr_tool.csv_tools._utils.CsvTool import CsvTool

from _xhr_tool.chromeRobot.src._chromeRobot_tool.dataUtils import DataUtils
from _xhr_tool.chromeRobot.src._chromeRobot_tool.decoratorUtils import DecoratorEngine
from _xhr_tool.chromeRobot.src._decorator._decorator import chrome_robot_excute, chrome_datas_catch
from _xhr_tool.chromeRobot.src.domain.Action2 import Action
from _xhr_tool.chromeRobot.src.domain.ChromeFactory import ChromeFactory
from _xhr_tool.chromeRobot.src.domain.HighterAction2 import HigherAction
class Tianyancha:
    savePath=relpath('../datasStore/天眼查/cccf.csv')
    cycleTimes=-1
    saveCsvHeads=['公司名','联系人','电话','地址', '城市', 'qq', '微信','邮箱','_url']
    #初始化
    # @chrome_robot_excute
    def test(self):
            HigherAction().click_byName(cssStr='.sup-ie-company-header-child-1 .link-click.link-spacing',name='查看更多').\
            selcetAction(action1=Action().find(cssStr='.phone',key='电话',mode='multiple',catchDate=True).clickXY(),
                         action2=Action().find(cssStr='.sup-ie-company-header-child-1 span:nth-child(4)',key='电话',catchDate=True)
                         ).excute(isSave=True)
        # HigherAction().find(cssStr='.phone',key='电话',mode='multiple').excute(isSave=True)


    @chrome_robot_excute
    def web(self):

        #取出所有公司名称，然后逐个验证
        HigherAction().jumpBrowserTab(index=-1).\
            key_input(cssStr="input[type='search']",text='福建百宏聚纤科技实业有限公司').\
            click(cssStr='.input-group-btn').\
            jumpBrowserTab(index=-1).\
            click(cssStr='.search-result-single em',index=0,loadNewPage=True).\
            jumpBrowserTab(index=-1). \
            find(cssStr=".name", key="公司名",catchDate=True). \
            find(cssStr=".name>.link-click", key="客户",catchDate=True). \
            find(cssStr=".auto-folder", key="地址",catchDate=True). \
            find(cssStr="tbody > tr:nth-child(11) > td:nth-child(2) > span", key="产品",catchDate=True). \
            find(cssStr=".summary", key="信息",catchDate=True). \
            find(cssStr=".-breakall > tbody > tr:nth-child(1) > td:nth-child(4)", key="资本",catchDate=True). \
            find(cssStr=".-breakall  tr:nth-child(5) > td:nth-child(4)", key="模式",catchDate=True).\
            findCurrentUrl(key='_url',catchDate=True).\
            find(cssStr=".tag-list", key="经营状况"). \
            click_byName(cssStr='.sup-ie-company-header-child-1 .link-click.link-spacing', name='查看更多'). \
            selcetAction(action1=Action().find(cssStr='.phone', key='电话', mode='multiple', catchDate=True).clickXY(),
                         action2=Action().find(cssStr='.sup-ie-company-header-child-1 span:nth-child(4)', key='电话',
                                               catchDate=True)).\
            excuteBlock(isSave=True)
    @chrome_datas_catch
    def dataSave(self,datas):
        print(datas)
if __name__ == '__main__':
    chromeFactory = ChromeFactory()
    chromeFactory.register(Tianyancha)


