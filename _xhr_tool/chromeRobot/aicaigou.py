from _xhr_tool.chromeRobot.src._decorator._decorator import chrome_robot_excute, chrome_datas_catch
from _xhr_tool.chromeRobot.src.domain.Action import Action
from _xhr_tool.chromeRobot.src.domain.ChromeFactory import ChromeFactory
from _xhr_tool.chromeRobot.src.domain.HighterAction import HigherAction


class Aaicaigou:
    @chrome_robot_excute
    def run(self):
        Action("爱采购").initWeb(url='https://b2b.baidu.com/'). \
            key_input(cssStr=".ivu-input", text="吊装带", isClear=True). \
            click(cssStr=".search-btn"). \
            excute()
        pass
    @chrome_robot_excute
    def test(self):
        def crapy(response):
            Action().jumpBrowserTab(index=-1).find(key='城市',cssStr='.address',catchDate=True).\
                find(key='联系人',cssStr='.details-sections-item .item-container:nth-child(2) .value',catchDate=True).\
                find(key='手机',cssStr='.details-sections-item .item-container:nth-child(3) .value',catchDate=True).\
                find(key='电子邮箱',cssStr='.details-sections-item .item-container:nth-child(4) .value',catchDate=True).\
                find(key='详细地址',cssStr='.details-sections-item .item-container:nth-child(6) .value',catchDate=True).\
                find(key='产品信息',cssStr='.rich-text.no-p-margin',catchDate=True).closeCurrentBroswserTab().putActionToReadyAct()
        Action("爱采购").find(key='公司名',cssStr='.p-card-desc-layout>div:last-child .name',mode='multiple',catchDate=True).excute()
        HigherAction().\
            thinking_click(cssStr='.p-card-desc-layout>div:last-child .name',sign='泰州市祥泰设备配套有限公司',index=10,func=crapy).excute()
    @chrome_datas_catch
    def data(self,datas):
        print(datas)
if __name__ == '__main__':
    chromeFactory = ChromeFactory()
    chromeFactory.register(Aaicaigou)

