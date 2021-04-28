import time
from _utils.RUtils import tool
from _xhr_tool.chromeRobot.src._decorator._decorator import chrome_robot_excute, chrome_datas_catch
from _xhr_tool.chromeRobot.src.domain.Action2 import Action
from _xhr_tool.chromeRobot.src.domain.ChromeFactory import ChromeFactory
from _xhr_tool.chromeRobot.src.domain.HighterAction2 import HigherAction
from _xhr_tool.mysql.connect import MySqlOptions
class Tianyancha:
    key_word = '吊装带'
    savePath='../datasStore/爱采购/爱采购爬虫_'+key_word+'.csv'
    cycleTimes=-1
    saveCsvHeads=['公司名','联系人','电话','地址', '城市', 'qq', '微信','邮箱','_url']
    # @chrome_robot_excute
    def test(self):
        Action().scroll_browser_top_to_button(cssStr='.ivu-page-next',elemntName='下一页',timeOut=60).excuteBlock()
        print('运行完毕')

    @chrome_robot_excute
    def web(self):
        HigherAction().initWeb(url='https://www.tianyancha.com/'). \
            key_input(cssStr="input[type='search']", text='福建百宏聚纤科技实业有限公司'). \
            click(cssStr='.input-group-btn'). \
            jumpBrowserTab(index=-1). \
            click(cssStr='.search-result-single em', index=0, loadNewPage=True). \
            jumpBrowserTab(index=-1). \
            find(cssStr=".name", key="公司名", catchDate=True). \
            find(cssStr=".name>.link-click", key="客户", catchDate=True). \
            find(cssStr=".auto-folder", key="地址", catchDate=True). \
            find(cssStr="tbody > tr:nth-child(11) > td:nth-child(2) > span", key="产品", catchDate=True). \
            find(cssStr=".summary", key="信息", catchDate=True). \
            find(cssStr=".-breakall > tbody > tr:nth-child(1) > td:nth-child(4)", key="资本", catchDate=True). \
            find(cssStr=".-breakall  tr:nth-child(5) > td:nth-child(4)", key="模式", catchDate=True). \
            findCurrentUrl(key='_url', catchDate=True). \
            find(cssStr=".tag-list", key="经营状况"). \
            excuteBlock(isSave=True)
            # click_byName(cssStr='.sup-ie-company-header-child-1 .link-click.link-spacing', name='查看更多'). \
            # selcetAction(action1=Action().find(cssStr='.phone', key='电话', mode='multiple', catchDate=True).clickXY(),
            #              action2=Action().find(cssStr='.sup-ie-company-header-child-1 span:nth-child(4)', key='电话',
            #                                    catchDate=True)). \

# @chrome_datas_catch
    def dataSave(self,datas):
        # 1.将此数据保存到爬虫配置文件中。
        obj={}
        for saveCsvHead in self.saveCsvHeads:
            obj.setdefault(saveCsvHead,datas.get(saveCsvHead))
        print(obj)
        #1.将公司信息存入数据库
        obj1=MySqlOptions().getTableDict(table='company')
        obj1['公司']=obj.get('公司名')
        obj1['地址']=obj.get('地址')
        obj1['关键词']=self.key_word
        obj1['爬虫网'] = '爱采购'
        obj1['reliability'] = 1
        if MySqlOptions().insert(table='company',objDict=obj1):
            tool().print('保存数据到表company_成功:'+str(obj1),fontColor='green')
        else:
            tool().print('保存数据到表company_失败:'+str(obj1),fontColor='red')
        #2.根据公司名查找其公司id
        id=MySqlOptions().find(table='company',columns=['id'],conditions=[("公司",obj1['公司'])])
        print(id)
        if id:
            id=id[0]
            obj2=MySqlOptions().getTableDict(table='customers')
            obj2['qq号']=obj.get('qq')
            obj2['邮箱']=obj.get('邮箱')
            obj2['微信号']=obj.get('微信')
            obj2['_url'] = obj.get('_url')
            obj2['客户']=obj.get('联系人')
            obj2['公司id']=id[0]
            obj2['手机1']=obj.get('电话')
            obj2['reliability']=1
            if MySqlOptions().insert(table='customers',objDict=obj2):
                tool().print('保存数据到表customers_成功:'+str(obj2),fontColor='green')
            else:
                tool().print('保存数据到表customers_失败:'+str(obj2),fontColor='red')
if __name__ == '__main__':
    chromeFactory = ChromeFactory()
    chromeFactory.register(Tianyancha)

