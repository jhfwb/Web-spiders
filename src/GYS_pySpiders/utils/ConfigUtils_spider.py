from scrapy.spiders import Rule

from src.GYS_pySpiders.utils.CommonUtils import CommonUtils
from src.GYS_pySpiders.utils.xmlUtils.configUtils import XmlConfigUtils
from scrapy.linkextractors import LinkExtractor

class SpidersConfigUitls:
    def __init__(self):
        self.xmlConfig=XmlConfigUtils()
        self.exec=self.xmlConfig.configDocumentObj['_children'][0]['exec']
        #取得指定的weisite
        self.website=self.xmlConfig.get('website',('webName',self.exec))

    def getRules(self):
        rules = self.website.getElementsByTagName("rules")[0].getElementsByTagName("rule")
        getRules = []
        for rule in rules:
            # CheckUtils.checkObje([bool(rule.getAttribute("follow"))],sleepTime=3,stop=True)
            getRules.append(
                Rule(
                    LinkExtractor(
                        allow=rule.getAttribute("allow")
                    ),
                    follow=CommonUtils.changeStrToBool(rule.getAttribute("follow")),
                    callback=rule.getAttribute("callback")
                )
            )
        return getRules

    def getDataCatch(self):
        datas=self.website.getElementsByTagName("dataCatch")[0].getElementsByTagName("data")
        arr=[]
        for data in datas:
            arr.append({"name":data.getAttribute("name"),"select":data.getAttribute("select")})
        return arr

    def getAllowed_domains(self):
        return [
            self.website.getAttribute(
                "allowed_domains")]

    def getStart_urls(self):
        return [
            self.website.getAttribute(
                "start_url")]

    def getFile(self):
        file = self.website.getElementsByTagName(
            "dataSave")[0].getElementsByTagName("file")[0]
        return {'path': file.getAttribute("path"), 'encoding': file.getAttribute("encoding")}