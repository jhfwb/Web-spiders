from _xhr_tool._utils import relpath
from _xhr_tool._utils.arr_caculate import remove_repeat_arr_inner_dict
from _xhr_tool.csv_tools._utils.CsvTool import CsvTool

from _xhr_tool.chromeRobot.src._chromeRobot_tool.dataUtils import DataUtils
from _xhr_tool.chromeRobot.src._chromeRobot_tool.decoratorUtils import DecoratorEngine
from _xhr_tool.chromeRobot.src._decorator._decorator import chrome_robot_excute, chrome_datas_catch
from _xhr_tool.chromeRobot.src.domain.Action2 import Action
from _xhr_tool.chromeRobot.src.domain.ChromeFactory import ChromeFactory
from _xhr_tool.chromeRobot.src.domain.HighterAction2 import HigherAction

class Cccf_crapy:
    savePath=relpath('../datasStore/水带厂/cccf2.csv')
    cycleTimes=-1
    saveCsvHeads=['公司名','联系人','电话','地址', '城市', 'qq', '微信','邮箱','_url']
    #初始化
    @chrome_robot_excute
    def web(self):
        def setPageNum(response):
            cycleTimes=int(response.datas.split('/')[1])
            self.cycleTimes=cycleTimes
        Action().initWeb(). \
            get("http://www.cccf.com.cn/certSearch/"). \
            key_input(cssStr="input[name=productName]", text="有衬里消防水带", isClear=True). \
            click(cssStr="input[type='submit']", ).jumpBrowserTab(index=-1).\
            find(cssStr='#searchForm   b:nth-child(2)',after_func=setPageNum).excuteBlock(isSave=False)

    @chrome_robot_excute
    def 循环点击下一页(self):
        for i in range(self.cycleTimes):
            def test2(response):
                if response.datas == '下一页':
                    return True
                else:
                    return False
            HigherAction().jumpBrowserTab(index=-1).\
                find(cssStr="td[valign='top'] tbody tr:nth-child(2) table td>div>div:nth-child(3)>div:nth-child(4)",
                     key="公司名称", mode='multiple', catchDate=True). \
                find(cssStr="td[valign='top'] tbody tr:nth-child(2) table td>div>div:nth-child(3)>div:nth-child(2)",
                     key="产品型号", mode='multiple', catchDate=True). \
                find(cssStr="td[valign='top'] tbody tr:nth-child(2) table td:nth-child(5) span", key="准入状态",
                     mode='multiple', catchDate=True). \
                click_byName(cssStr='#searchForm  table:nth-child(11) td:nth-child(2) a',name='下一页',ignoreErr=False).excute(isSave=True)

    @chrome_datas_catch
    def dataSave(self, datas):
        datas = DataUtils().datasChange(datas)  # 将数据形式进行更改
        # 数据遍历
        def test(x):
            x['公司名称'] = x['公司名称'].replace('认证委托人 ：', '')
            return x
        DataUtils().datasHandle(func=test, datas=datas)
        #自身数据数据去重
        datas = remove_repeat_arr_inner_dict(datas, key='公司名称')
        #取出
        keys = CsvTool().getCsvDatasByKey(path=self.savePath,key='公司名称',isCreateFile=True)
        datas=list(filter(lambda x:None if x['公司名称'] in keys else x,datas))
        if len(datas)!=0:
            CsvTool().optionCsv(datas=datas, path=self.savePath, isCreateFile=True, mode='a')
            print(datas)


if __name__ == '__main__':
    chromeFactory = ChromeFactory()
    chromeFactory.register(Cccf_crapy)


