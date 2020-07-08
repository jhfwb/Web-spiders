# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
import time
import re
from clientScrapySystem.webScrapySystem.GYS_pySpiders.Action import Store
from clientScrapySystem.webScrapySystem.GYS_pySpiders.utils.CommonUtils import CommonUtils
from clientScrapySystem.webScrapySystem.GYS_pySpiders.GYS_pySpiders.items import  顺企网Item
from clientScrapySystem.webScrapySystem.GYS_pySpiders.utils.ConfigUtils_spider import SpidersConfigUitls
from clientScrapySystem.webScrapySystem.GYS_pySpiders.utils.RR_Comments import PrintTool


class APyspiderSpider(CrawlSpider):
    name = '顺企网'
    config = Store.take(name, SpidersConfigUitls(webName=name))  # 在Stroue中创建一个对象。如果有就创建，没有就
    rules = config.getRules()
    allowed_domains = config.getAllowed_domains()
    start_urls = config.getStart_urls()
    PrintTool.print("爬虫"+name+"开始采集信息!!", fontColor="green")
    def __init__(self, *args, **kwargs):
        super(APyspiderSpider, self).__init__(*args, **kwargs)
    # def parse_item(self, response):
    #         self.myResponse=response
    #         # self.loadDate(response)
    #         datas=self.config.getDataCatch()
    #
    #         ##下面这串代码比较难理解。实际上是拼出了字符串。"GysPyspidersItem(公司名=self.公司名,地址=self.地址,固定电话=self.固定电话,主营产品=self.主营产品,客户=self.客户,手机号=self.手机号,公司网站 = self.公司网站,公司简介 =self.公司简介,电子邮箱 = self.电子邮箱,经营模式 = self.经营模式,企业类型 = self.企业类型,城市 = self.城市,公司规模 =self.公司规模,注册资本 = self.注册资本,来源网站= self.来源网站,信息获取的来源url= self.信息获取的来源url,记录时间= self.记录时间,)"
    #         ##并且这些字符串的获取都是从config配置文件中获取的。
    #         line="顺企网Item(_url=response.url,"
    #         for data in datas:
    #             line+=data['name']+"=self.selectElementStr('"+data['select']+"'),"
    #         line+=')'
    #         item=eval(line)
    #         print(self.name+"_爬虫 成功获得以下数据！！"+time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())+"\n",item)
    #         yield item
    #     #一般只要修改这里的数值就可以啦
    def parse_item(self, response):
            self.myResponse=response
            # self.loadDate(response)
            datas=self.config.getDataCatch()
            ##下面这串代码比较难理解。实际上是拼出了字符串。"GysPyspidersItem(公司名=self.公司名,地址=self.地址,固定电话=self.固定电话,主营产品=self.主营产品,客户=self.客户,手机号=self.手机号,公司网站 = self.公司网站,公司简介 =self.公司简介,电子邮箱 = self.电子邮箱,经营模式 = self.经营模式,企业类型 = self.企业类型,城市 = self.城市,公司规模 =self.公司规模,注册资本 = self.注册资本,来源网站= self.来源网站,信息获取的来源url= self.信息获取的来源url,记录时间= self.记录时间,)"
            ##并且这些字符串的获取都是从config配置文件中获取的。
            line="顺企网Item(_url=response.url,_catchTime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),"
            mode=""
            mutiplateArrs=[]
            for data in datas:
                if data.get('mode')=='mutiplate':
                    mode='mutiplate'
                    mutiplateArrs.append(data.get('name'))
                line += data['name'] + "=self.selectElementStr('" + data['select'] + "'," + str(data.get('mode')) + "),"
            line+=')'
            item=eval(line)
            #待优化
            sitekey=""
            if mode=='mutiplate':
                items = []
                itemMutiplateArr = {}
                for mutiplateArr in mutiplateArrs:
                    itemMutiplateArr.setdefault(mutiplateArr, CommonUtils.changeStrToList(item[mutiplateArr]))
                for key in item.keys():
                    if key in mutiplateArrs:
                        its=CommonUtils.changeStrToList(item[key])
                        for itf in its:
                            items.append({key:itf})
                        sitekey=key
                        break
                for i in range(len(items)):
                    templates=[]
                    for key1 in item.keys():
                        if key1 in mutiplateArr:
                            if key1!=sitekey:
                                try:
                                    items[i].setdefault(key1,itemMutiplateArr[key1][i])
                                except:
                                    raise ValueError("mutiplate的长度不一致！"+ items)
                        else:
                            items[i].setdefault(key1,item[key1])
                # 待优化
                for item in items:
                    print(self.name + "_爬虫 成功获得以下数据！！" + time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()) + "\n",
                          item)
                    yield item
            else:
                print(self.name+"_爬虫 成功获得以下数据！！"+time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())+"\n",item)
                print(item)
                yield item
        #一般只要修改这里的数值就可以啦
    def loadDate(self,response):##弃用！！！
        # print(self.configDocument)
        self['']
        self.公司名 = self.selectElementStr("#logoco > h1 > span")
        self.地址 = self.selectElementStr("#contact > div > dl > dd:nth-child(2)")
        self.固定电话 = self.selectElementStr("#contact > div > dl > dd:nth-child(4)")
        self.主营产品 = self.selectElementStr("#gongshang > div > table >  tr:nth-child(2) > td:nth-child(2)")
        self.客户 = self.selectElementStr("#contact > div > dl > dd:nth-child(6)")
        self.手机号 = self.selectElementStr("#contact > div > dl > dd:nth-child(8)")
        self.公司网站 = ""
        self.公司简介 = ""  # response.css("#aboutuscontent::text").extract()[0],
        self.电子邮箱 = self.selectElementStr("#contact > div > dl > dd:nth-child(10)")
        self.经营模式 = ""
        self.企业类型 = ""
        self.城市 = ""
        self.公司规模 = ""
        self.注册资本 = ""
        self.来源网站 = "顺企网"
        self.信息获取的来源url = response.url
        self.记录时间 = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
    #只要取得选择器，就能获得这个选择器当中的所有文本
    def selectElementStr(self, selecterStr, mode):
        try:
            arr = self.myResponse.css(selecterStr).extract()
            if mode == "mutiplate":
                textArr = []
                if len(arr) > 1:
                    for text in arr:
                        if text.strip() != "":
                            newStr = re.sub(r'<!--[\s\S]*?-->', "", text).strip()
                            newStr = re.sub(r'<.*?>', "", newStr).strip()
                            textArr.append(newStr)
                    newStr = str(textArr)
                else:
                    newStr = re.sub(r'<.*?>', "", arr[0]).strip()
            else:
                if len(arr) > 1:
                    for text in arr:
                        if text.strip() != "":
                            newStr = re.sub(r'<.*?>', "", text).strip()
                            break
                else:
                    newStr = re.sub(r'<.*?>', "", arr[0]).strip()
        except:
            newStr = ""

        return newStr