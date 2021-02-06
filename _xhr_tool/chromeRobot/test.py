from _xhr_tool.chromeRobot.src._decorator._decorator import chrome_robot_excute, chrome_datas_catch
from _xhr_tool.chromeRobot.src.domain.Action import Action
from _xhr_tool.chromeRobot.src.domain.ChromeFactory import ChromeFactory


class TestC:
    @chrome_robot_excute
    def run(self):
        """你好
        :params s:你好
        """
        Action("获得百度信息").get(url='https://www.baidu.com/') \
     .find(key='1',cssStr='.hotsearch-item',elementsIndex=1,mode="single",func=TestC().test)\
            .find(key='1',cssStr='.hotsearch-item',elementsIndex=2,mode="single").excute()
        # Action("天眼查搜 寻公司信息").get(web='https://b2b.baidu.com/s?q=%E5%90%8A%E8%A3%85%E5%B8%A6&from=search')\
        #     .find(cssStr='div.card-layout.inline.is-wide span.name>span',mode='multiple').excute(

    def test(self,response):

        # Action(memo="获得百度信息",callBackFunc=lambda x:print('我完成回调了！')).get(url='https://www.baidu.com/s?cl=3&tn=baidutop10&fr=top1000&wd=%E6%8B%9C%E7%99%BB%E5%B0%86%E9%87%8D%E6%96%B0%E8%AF%84%E4%BC%B0%E4%B8%AD%E7%BE%8E%E7%BB%8F%E8%B4%B8%E5%8D%8F%E8%AE%AE&rsv_idx=2&rsv_dl=fyb_n_homepage&hisfilter=1').excuetNow()
        Action("获得百度信息").find(key='立即实行',cssStr='.hotsearch-item',elementsIndex=5,mode="single").excuteActionRightNow()
        return response

    @chrome_robot_excute
    def run2(self):
        """你好
        :params s:你好
        """
        pass
    @chrome_datas_catch
    def data(self,item):
        # return
        print(item)
if __name__ == '__main__':
    chromeFactory = ChromeFactory()
    chromeFactory.register(TestC)
