import time
from _utils.RUtils import tool
from _xhr_tool.chromeRobot.src._decorator._decorator import chrome_robot_excute, chrome_datas_catch
from _xhr_tool.chromeRobot.src.domain.Action2 import Action
from _xhr_tool.chromeRobot.src.domain.ChromeFactory import ChromeFactory
from _xhr_tool.chromeRobot.src.domain.HighterAction2 import HigherAction
from _xhr_tool.chromeRobot.src.servlet.robot_thread import MyPipelineThread
from _xhr_tool.csv_tools._utils.CsvTool import CsvTool
from _xhr_tool.excuteEngine.Engine import ExcuteFuel
from _xhr_tool.mysql.connect import MySqlOptions
class Aaicaigou:
    def __init__(self,key_word):
        self.key_word = key_word
        self.savePath = '../datasStore/爱采购/爱采购爬虫_' + self.key_word + '.csv'
        self.cycleTimes = -1
        self.saveCsvHeads = ['公司名', '联系人', '电话', '地址', '城市', 'qq', '微信', '邮箱', '_url']
        self.sqlOption=MySqlOptions(host='localhost', user='root', password='512124632', database='crapydatabase')
    # @chrome_robot_excute
    def test(self):
        Action().scroll_browser_top_to_button(cssStr='.ivu-page-next',elemntName='下一页',timeOut=60).excuteBlock()
        print('运行完毕')

    @chrome_robot_excute
    def web(self):
        HigherAction().initWeb(url='https://b2b.baidu.com/').\
            click(cssStr='.ivu-icon.ivu-icon-ios-close',ignoreErr=True).\
            key_input(cssStr=".ivu-input", text=self.key_word, isClear=True). \
            click(cssStr=".search-btn"). \
            jumpBrowserTab(index=-1).excute()
    @chrome_robot_excute
    def webInit(self):#初始化
        def test(response):
            if response.datas=='' or response.datas==None:
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
            ).closeCurrentBroswserTab().excuteRightNow(isSave=True)
        for i in range(self.cycleTimes):
            def _isClick(name):
                _a=self.sqlOption.find(table='company',columns=['公司'],conditions=[('公司',name)])
                if len(_a)!=0:
                    print('该公司已存在:'+name)
                    return False
                else:
                    return True
            HigherAction().\
            click_all_except_crapyedDatas2(cssStr='.s-content .p-card-desc-layout>div:last-child .name',func=crapy,before_click_func=_isClick).\
            click(cssStr='.ivu-page-next',ignoreErr=False).scroll_browser_top_to_button(cssStr='.ivu-page-next',elemntName='下一页',timeOut=60).excuteBlock()
            tool().print('...开始运行下一页...')
        print('运行结束')
    @chrome_datas_catch
    def dataSave(self,datas):
        # 1.将此数据保存到爬虫配置文件中。
        obj={}
        for saveCsvHead in self.saveCsvHeads:
            obj.setdefault(saveCsvHead,datas.get(saveCsvHead))
        #1.将公司信息存入数据库
        obj1=self.sqlOption.getTableDict(table='company')
        obj1['公司']=obj.get('公司名')
        obj1['地址']=obj.get('地址')
        obj1['关键词']=self.key_word
        obj1['数据来源'] = '爱采购'
        obj1['reliability'] = 1
        if self.sqlOption.insert(table='company',objDict=obj1):
            tool().print('保存数据到表company_成功:'+str(obj1),fontColor='green')
        else:
            tool().print('保存数据到表company_失败:'+str(obj1),fontColor='red')
        #2.根据公司名查找其公司id
        id=self.sqlOption.find(table='company',columns=['id'],conditions=[("公司",obj1['公司'])])
        if id:
            id=id[0]
            obj2=self.sqlOption.getTableDict(table='customers')
            obj2['qq号']=obj.get('qq')
            obj2['邮箱']=obj.get('邮箱')
            obj2['微信号']=obj.get('微信')
            obj2['_url'] = obj.get('_url')
            obj2['客户']=obj.get('联系人')
            obj2['公司id']=id[0]
            obj2['手机1']=obj.get('电话')
            obj2['reliability']=1
            if self.sqlOption.insert(table='customers',objDict=obj2):
                tool().print('保存数据到表customers_成功:'+str(obj2),fontColor='green')
            else:
                tool().print('保存数据到表customers_失败:'+str(obj2),fontColor='red')
if __name__ == '__main__':
    arr=['压膜带','高强涤纶','渔网','缆绳','捆绑带','滤布','土工布',
         '涤纶工业丝','胶管','吊装带','土工格栅',
         '软管','特斯林','宠物带','安全带','安全绳',
         '绳缆','涂层布','打包带','拖车带','消防水带','农用水带','打包带'
        ,'绳缆','箱包布','遮阳布','帘子线','高强缝纫线','蓬盖布']
    chromeFactory = ChromeFactory()
    # chromeFactory.register(Aaicaigou('高强涤纶'))
    # map(lambda x:chromeFactory.register(Aaicaigou(x)),arr)
    for a in arr:
        chromeFactory.register(Aaicaigou(a))

