# -*- coding: utf-8 -*-
# Define here the models for your scraped items
# 模板：替换位置：__spiderName__替换成spider的名称
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from src.GYS_pySpiders.Action import Store
from src.GYS_pySpiders.utils.ConfigUtils_spider import SpidersConfigUitls
class 顺企网Item(scrapy.Item):
    actionConfigUtils = Store.take('顺企网', SpidersConfigUitls(webName='顺企网'))
    datas=actionConfigUtils.getDataCatch()
    for data in datas:
        exec(data['name']+"=scrapy.Field()")
    _url=scrapy.Field()
    # 公司名 = scrapy.Field()
    # 地址 = scrapy.Field()
    # 固定电话 = scrapy.Field()
    # 主营产品 = scrapy.Field()
    # 客户= scrapy.Field()
    # 手机号 = scrapy.Field()
    # 公司网站= scrapy.Field()
    # 公司简介= scrapy.Field()
    # 电子邮箱= scrapy.Field()
    # 经营模式= scrapy.Field()
    # 企业类型= scrapy.Field()
    # 城市= scrapy.Field()
    # 公司规模= scrapy.Field()
    # 注册资本= scrapy.Field()
    # 来源网站= scrapy.Field()
    # 记录时间= scrapy.Field()
    # 信息获取的来源url= scrapy.Field()
class 招商100Item(scrapy.Item):
    actionConfigUtils = Store.take('招商100', SpidersConfigUitls(webName='招商100'))
    datas=actionConfigUtils.getDataCatch()
    for data in datas:
        exec(data['name']+"=scrapy.Field()")
    _url=scrapy.Field()
    # 公司名 = scrapy.Field()
    # 地址 = scrapy.Field()
    # 固定电话 = scrapy.Field()
    # 主营产品 = scrapy.Field()
    # 客户= scrapy.Field()
    # 手机号 = scrapy.Field()
    # 公司网站= scrapy.Field()
    # 公司简介= scrapy.Field()
    # 电子邮箱= scrapy.Field()
    # 经营模式= scrapy.Field()
    # 企业类型= scrapy.Field()
    # 城市= scrapy.Field()
    # 公司规模= scrapy.Field()
    # 注册资本= scrapy.Field()
    # 来源网站= scrapy.Field()
    # 记录时间= scrapy.Field()
    # 信息获取的来源url= scrapy.Field()
