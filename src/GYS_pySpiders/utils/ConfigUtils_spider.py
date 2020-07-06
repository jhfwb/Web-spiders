from scrapy.spiders import Rule
from src.GYS_pySpiders.utils.CommonUtils import CommonUtils
from src.GYS_pySpiders.utils.RR_Comments import PrintTool
from src.GYS_pySpiders.utils.xmlUtils.configUtils import XmlConfigUtils
from scrapy.linkextractors import LinkExtractor
class SpidersConfigUitls:
    def __init__(self,webName=""):
        """
        传入webName。它会根据webName。自动将对应的web赋值到self.website中。如果webName没有传入。则默认赋值第一个。
        """
        self.xmlConfig=XmlConfigUtils()
        self.xmlConfig.getDocumentObj()
        #获取执行数组。
        self.execs=self._getExecArr(self.xmlConfig.get(documentObj=self.xmlConfig.getDocumentObj(),_name='spiders'))
        self.website=""
        #取得指定的weisite
        for i in range(len(self.execs)):
            # PrintTool.print(self.execs[i],fontColor='yellow')

            try:
                if webName==self.execs[i]['webName']:
                    self.website = self.execs[i]
                    break
            except:
                raise ValueError("在配置文档中，没有找到该website的webName属性。请确保添加了webName属性。"+str(self.website))
        if self.website=="":
            PrintTool.print('警告:没有找到该websit:'+self.website+"。已经自动为其赋值为首个website:"+self.execs[0]['webName'])
            self.website=self.execs[0]
        PrintTool.print(self.website, fontColor='yellow')
    def changeWebsite(self,index):
        self.website=self.execs[index]
    def _getExecArr(self,spiderObj):
        """
        获取需要执行的website对象。spiderObj是一个spider对象
        @parm spiderObj
        """
        spisersTag = spiderObj
        print(spiderObj)
        websites = spisersTag['_children']
        execWebsites = []
        for i in range(len(websites)):
            print(websites[i])
            if 'exec' in websites[i].keys():
                if websites[i]['exec'] == "True":
                    execWebsites.append(websites[i])
        return execWebsites
    def getRules(self):
        rules = self.xmlConfig.get(documentObj=self.website, _name='rule')
        # rules = self.website.getElementsByTagName("rules")[0].getElementsByTagName("rule")
        getRules = []
        for rule in rules:
            # CheckUtils.checkObje([bool(rule.getAttribute("follow"))],sleepTime=3,stop=True)
            callback=rule.get("callback")
            if callback:
                pass
            else:
                callback=""
            dont_filter=rule.get("dont_filter")
            if not dont_filter:
                dont_filter=False
            getRules.append(
                Rule(
                    LinkExtractor(
                        allow=rule["allow"],

                    ),
                    follow=CommonUtils.changeStrToBool(rule["follow"]),
                    callback=callback,
                    # dont_filter=bool(dont_filter),
                )
            )
        return getRules
    def getDataCatch(self):
        datas=self.xmlConfig.get(documentObj=self.website,_name='data')
        arr=[]
        for data in datas:
            arr.append({"name":data['name'],"select":data["select"]})
        return arr
    def getAllowed_domains(self):
        return [
            self.website['allowed_domains']
        ]
    def getStart_urls(self):
        """

        """
        if type(self.website['start_url'])==type([]):
            return self.website['start_url']
        if type(self.website['start_url']) == type(""):
            return [self.website['start_url']]
        else:
            raise ValueError('start_url格式错误！既不是字符串，也不是数组')

    def getFile(self):
        file=self.xmlConfig.get(documentObj=self.website, _name='file')
        # file = self.website.getElementsByTagName(
        #     "dataSave")[0].getElementsByTagName("file")[0]


        return {'path': file["path"], 'encoding': file["encoding"]}