from _utils.RUtils import tool

from _xhr_tool._utils import relpath
from _xhr_tool._utils.arr_caculate import remove_repeat_arr_inner_dict
from _xhr_tool.csv_tools._utils.CsvTool import CsvTool
import difflib
from _xhr_tool.chromeRobot.src._chromeRobot_tool.dataUtils import DataUtils
from _xhr_tool.chromeRobot.src._chromeRobot_tool.decoratorUtils import DecoratorEngine
from _xhr_tool.chromeRobot.src._decorator._decorator import chrome_robot_excute, chrome_datas_catch
from _xhr_tool.chromeRobot.src.domain.Action2 import Action
from _xhr_tool.chromeRobot.src.domain.ChromeFactory import ChromeFactory
from _xhr_tool.chromeRobot.src.domain.HighterAction2 import HigherAction
from _xhr_tool.mysql.connect import MySqlOptions
class Tianyancha:
    savePath=relpath('../datasStore/天眼查/cccf.csv')
    saveCsvHeads=['公司名','联系人','电话','地址', '城市', 'qq', '微信','邮箱','_url']
    #初始化
    def __init__(self,company,sqlOption):
        self.company=company
        self.sqlOption=sqlOption
        pass
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
            key_input(cssStr="input[type='search']",text=self.company).\
            click(cssStr='.input-group-btn').\
            jumpBrowserTab(index=-1).\
            click(cssStr='.search-result-single em',index=0,loadNewPage=True).\
            jumpBrowserTab(index=-1). \
            find(cssStr=".name>.link-click", key="客户",catchDate=True,ignoreErr=False). \
            find(cssStr=".name", key="公司", catchDate=True). \
            find(cssStr=".auto-folder", key="地址",catchDate=True). \
            find(cssStr="tbody > tr:nth-child(11) > td:nth-child(2) > span", key="产品信息",catchDate=True). \
            find(cssStr=".-breakall > tbody > tr:nth-child(1) > td:nth-child(4)", key="经营状况",catchDate=True). \
            find(cssStr=".-breakall tr:nth-child(4) > td:nth-child(2)", key="实缴资本", catchDate=True). \
            find(cssStr=".-breakall tr:nth-child(3) > td:nth-child(2)", key="注册资本", catchDate=True). \
            find(cssStr=".-breakall  tr:nth-child(7) > td:nth-child(4)", key="行业",catchDate=True).\
            find(cssStr=".email", key="邮箱",catchDate=True).\
            find(cssStr=".company-link", key="公司网址",catchDate=True).\
            findCurrentUrl(key='_url',catchDate=True).\
            click_byName(cssStr='.sup-ie-company-header-child-1 .link-click.link-spacing', name='查看更多'). \
            selcetAction(action1=Action().find(cssStr='.phone', key='电话', mode='multiple', catchDate=True).clickXY(),
                         action2=Action().find(cssStr='.sup-ie-company-header-child-1 .label +div+span', key='电话',catchDate=True)).\
            closeCurrentBroswserTab().\
            excuteBlock(isSave=True)
    @chrome_datas_catch
    def dataSave(self,datas):
        if datas=={}:
            obj = self.sqlOption.getTableDict(table='company')
            obj['数据状态'] = 'bug'
            sqlOption.update_obj(table='company', obj=obj, uniqueCondition=[('公司', self.company)])
            tool().print('出现bug，已经重新定义该数据')
            return
        if difflib.SequenceMatcher(None, datas['公司'], self.company).quick_ratio()>0.9:#比较数据库中的公司名称与天眼查的公司名称的相似度，达到0.9才会录进去
            obj=self.sqlOption.getTableDict(table='company')
            print(datas)
            obj['公司']=datas['公司']
            obj['公司简介']=datas['产品信息']
            obj['地址']=datas['地址']
            obj['经营状况']=datas['经营状况']
            obj['注册资本']=datas['注册资本']
            obj['实缴资本']=datas['实缴资本']
            obj['行业']=datas['行业']
            obj['客户']=datas['客户']
            obj['邮箱']=datas.get('邮箱')
            obj['公司网址']=datas.get('公司网址')
            obj['电话集']=datas.get('电话')
            obj['数据状态']='天眼查已查证'
            if obj['电话集']!=None:
                电话集=obj['电话集']
                if type(电话集)!=type([]):
                    电话集=[电话集]
                if len(电话集)!=0:
                    电话集=list(filter(lambda x:len(x)==11,电话集))[0:3]
                    for i in range(0,len(电话集)):
                        obj['电话'+str(i+1)]=电话集[i]
            try:
                sqlOption.update_obj(table='company',obj =obj,uniqueCondition=[('公司',self.company)])
                tool().print('保存数据成功:' + str(obj))
            except Exception:

                obj = self.sqlOption.getTableDict(table='company')
                obj['数据状态'] = 'bug'
                sqlOption.update_obj(table='company', obj=obj, uniqueCondition=[('公司', self.company)])
                tool().print('出现bug，已经重新定义该数据')

        else:#相似度不够
            obj=self.sqlOption.getTableDict(table='company')
            obj['数据状态']='天眼查已查证_相似度不足'
            sqlOption.update_obj(table='company', obj=obj, uniqueCondition=[('公司', self.company)])
            tool().print('保存数据失败,相似度不足:' + str(self.company)+"与"+str(datas['公司']))
if __name__ == '__main__':
    chromeFactory = ChromeFactory()
    sqlOption = MySqlOptions(host='localhost', user='root', password='512124632', database='crapydatabase')
    print(sqlOption.getTableDict(table='company'))
    datas=sqlOption.find_tables(table='company',conditions=[('数据状态','未知数据')],columns=['公司'])
    # 需天眼查查验
    for data in datas[1:]:
        chromeFactory.register(Tianyancha(data[0],sqlOption))



