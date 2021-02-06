from _xhr_tool._utils import relpath
from _xhr_tool._utils.CsvTool import CsvTool
from _xhr_tool.chromeRobot.src._chromeRobot_tool import DataUtils
from _xhr_tool.chromeRobot.src._decorator._decorator import chrome_robot_excute, chrome_datas_catch
from _xhr_tool.chromeRobot.src.domain.Action import Action
from _xhr_tool.chromeRobot.src.domain.ChromeFactory import ChromeFactory

from _xhr_tool.chromeRobot.src.domain.ExcuteResponse import ExcuteResponse
from _xhr_tool.chromeRobot.src.domain.HighterAction import HigherAction


class TestC:
    @chrome_robot_excute
    def run(self):
        pass
        Action("天眼查搜寻公司信息").initWeb(). \
            get("http://www.cccf.com.cn/certSearch/"). \
            key_input(cssStr="input[name=productName]", text="有衬里消防水带", isClear=True). \
            click(cssStr="input[type='submit']", ). \
            jumpBrowserTab(index=1).\
            excute()
            # click(cssStr="td[align='right'] a:nth-child(2)"). \

    @chrome_robot_excute(times=280)
    def 循环点击下一页(self):
        def test2(response:ExcuteResponse):
            if response.datas=='下一页':
                return True
            else:
                return False

        action=HigherAction("")
        action. \
        find(cssStr="td[valign='top'] tbody tr:nth-child(2) table td>div>div:nth-child(3)>div:nth-child(4)",
             key="公司名称", mode='multiple'). \
        find(cssStr="td[valign='top'] tbody tr:nth-child(2) table td>div>div:nth-child(3)>div:nth-child(2)",
             key="产品型号", mode='multiple').\
        find(cssStr="td[valign='top'] tbody tr:nth-child(2) table td:nth-child(5) span", key="准入状态",
                 mode='multiple').\
        find(cssStr="td:last-child a:nth-child(3)",func=test2,catchDate=False).\
        selcetAction(action1=Action().click(cssStr='td:last-child a:nth-child(3)'),
                         action2=Action().click(cssStr="table:nth-child(2) tr:nth-child(2)  table:nth-child(11) > tbody > tr > td:nth-child(2) > a:nth-child(2)")).excute()
    @chrome_datas_catch
    def data(self,datas):
        datas=DataUtils().datasChange(datas) #将数据形式进行更改
                                            #数据遍历
        def test(x):
            x['公司名称'] = x['公司名称'].replace('认证委托人 ：','')
            return x
        DataUtils().datasHandle(func=test,datas=datas)
        # {}['公司名称']={}['公司名称'].replace('','认证委托人 ：')

        CsvTool().optionCsv(datas=datas,path=relpath('datasStore/水带厂家.csv'),isCreateFile=True,mode='a')


            # for next in list(data.items())[0]:
            #     item.setdefault()



        pass
if __name__ == '__main__':
    chromeFactory = ChromeFactory()
    chromeFactory.register(TestC)

    # print(a)
