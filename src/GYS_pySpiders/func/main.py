from scrapy.cmdline import execute

from src.GYS_pySpiders.utils.ConfigUtils_spider import SpidersConfigUitls
from src.GYS_pySpiders.utils.xmlUtils.configUtils import XmlConfigUtils


class Func:
    def __init__(self):
        self.configUtils =SpidersConfigUitls()

    def scrapying(self, webName=""):  #
        """
        开始爬虫
        """
        if webName == "":
            pass
        else:
            execWeb = self.configUtils.xmlConfig.configDocumentObj['_children'][0]['exec']
            if execWeb==webName:
                pass
            else:
                self.configUtils.xmlConfig.configDocumentObj['_children'][0]['exec']=webName
                self.configUtils.xmlConfig.updata()
        execute(['scrapy', 'crawl', '_pySpider'])
        pass

    def addScrapyWeb(self, options={'webName': 'None',
                                    'start_url': '',
                                    'allowed_domains': '',
                                    'rules': [
                                        {
                                            'allow': '', 'follow': ''
                                        }
                                    ],
                                    'selectors': [
                                        {
                                            'name': '',
                                            'select': ''
                                        }
                                    ],
                                    'filePath': ''
                                    }):
        """
        :param
        webName:网站名称 不允许重复
        start_url:网站开始的名称
        allowed_domains:允许爬虫的域名
        scrapyName:爬虫的名字
        rules：爬虫的规则[(re,follow),] re:正则。follow:是否跟进(只允许一个不跟进)
        selectorsAndKey:选择器和字段名称

        检车是否可以使用
        :return
        """
        rules = []
        for rule in options['rules']:  # 添加rule
            rule.setdefault('_name', 'rule')
            if rule['follow'] == False:
                rule.setdefault('callback', 'parse_item')
            rules.append(rule)
        dataCatch = []
        for selector in options['selectors']:
            selector.setdefault('_name', 'data')
            dataCatch.append(selector)
        obj = {
            'webName': options['webName'],
            'start_url': options['start_url'],
            'allowed_domains': options['allowed_domains'],
            '_name': 'website',
            '_children': [
                {
                    '_name': 'rules',
                    '_children': rules
                },
                {
                    '_name': 'dataCatch',
                    '_children': dataCatch
                },
                {
                    '_name': 'dataSave',
                    '_children': [
                        {
                            '_name': 'file',
                            'path': options['filePath'],
                            'encoding': ''
                        }
                    ]
                }
            ]
        }
        # 将这个obj添加到虚拟文档中
        self._getConfigDocumentObjWebsites().append(obj)
        # 更新
        self.configUtils.updata()

    def removeScrapyWeb(self, webName):
        def remove(self):
            arr = self._getConfigDocumentObjWebsites()
            for i in range(0, len(arr)):
                if arr[i]['webName'] == webName:
                    self._getConfigDocumentObjWebsites().remove(arr[i])
                    return True
            # 移除脚本
            return False

        if remove(self) == True:
            self.configUtils.updata()
        else:
            print("无此元素，删除事变")

    def _getConfigDocumentObjWebsites(self):
        """
        中间方法:返回当前所有website对象
        """
        return self.configUtils.configDocumentObj['_children'][0]['_children']

    def modifyScrapyWeb(self, webName, ):
        pass

    def displayScrapyWeb(self, webName):
        """
        根据名称（webName）返回一个obj内存对象对象
        """
        website = self.configUtils.get('website', ('webName', webName))  # 获得website的DOM Element对象
        websiteObj = self.configUtils.loadObjectByTag(website)  # 获得该对象的Obj
        return websiteObj


if __name__ == '__main__':
    a = Func()
    a.scrapying('顺企网')
    # a.addScrapyWeb()
    # a.removeScrapyWeb('None')
    # print(Func().removeScrapyWeb('None'))
    # a._getConfigDocumentObjWebsite()
