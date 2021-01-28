from _xhr_tool.chromeRobot._decorator._decorator import chrome_robot_excute, chrome_datas_catch
from _xhr_tool.chromeRobot.domain.Action import Action
from _xhr_tool.chromeRobot.domain.ChromeFactory import ChromeFactory
import inspect
class TestC:
    @chrome_robot_excute
    def run(self):
        """你好
        :params s:你好
        """
        Action("天眼查搜 寻公司信息").get(web='https://www.baidu.com/').find(cssStr='#hotsearch-content-wrapper > li:nth-child(1) > a > span.title-content-title').excute()

    @chrome_robot_excute
    def run2(self):
        """你好
        :params s:你好
        """
        Action("天眼查搜 寻公司信息").get(web='https://www.baidu.com/').find(
            cssStr='#hotsearch-content-wrapper > li:nth-child(1) > a > span.title-content-title').excute()

    @chrome_datas_catch
    def data(self,item):
        print(item)
if __name__ == '__main__':

    chromeFactory = ChromeFactory()
    chromeFactory.register(TestC)
