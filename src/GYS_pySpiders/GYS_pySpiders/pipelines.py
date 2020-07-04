# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import time
import csv
import unicodedata

from src.GYS_pySpiders.utils.ConfigUtils_spider import SpidersConfigUitls
from src.GYS_pySpiders.utils.RR_Comments import PrintTool
from src.GYS_pySpiders.utils.xmlUtils.configUtils import XmlConfigUtils
class GysPyspidersPipeline(object):
    def __init__(self):
        # print("我运行了，但是我只运行一次！！！！！！！！！！！！！！！！！！！！！！！！！")
        pass
    def open_spider(self, spider):
        # x = Action.configUtils[spider.name]  # 如果只运行一次就不好了
        x=spider.config
        file = x.getFile()
        # PrintTool.print(fileName,fontColor='red')
        self.fileName = file['path']
        self.unicode = file['encoding']
        print("爬虫"+spider.name+"已经开始，开始时间:"+str(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())))
        spider.startTime=time.time()
        spider.fileName=self.fileName

        spider.unicode = self.unicode
        fileName=self.fileName
        unicode=self.unicode
        self.headers=[]
        datas = spider.config.getDataCatch()

        for data in datas:
            self.headers.append(data['name'])
        self.headers.append('_url')


        # 如果不存在就创建一个新的文件
        if os.path.exists(fileName)==False:
            self.fp = open(fileName, "a", encoding=unicode)
            self.fp.close()
        # 读取这个文件，判断这个文件是否有第一行，如果没有则创建首行，如果有则不创建，并关闭这个流
        self.fp = open(fileName, "r", encoding=unicode)
        if self.fp.readline()=="":
            self.fp.close()

            self.fp = open(fileName, "w", encoding=unicode,newline="")
            writer = csv.DictWriter(self.fp, self.headers)
            writer.writeheader()
        self.fp.close()
        # 打开添加的流

        self.fp=open(fileName, "a", encoding=unicode,newline="")
    def process_item(self, item, spider):
        writer = csv.DictWriter(self.fp, self.headers)
        try:
            writer.writerow(item)
        except:
            for key in item.keys():
                item[key]=unicodedata.normalize('NFKC', item[key])

            PrintTool.print(item,fontColor='pink')
            writer.writerow(item)
        self.fp.flush()
    def close_spider(self, spider):
        writer = csv.DictWriter(self.fp, self.headers)
        print("爬虫pipieline已经关闭，结束时间"+str(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())))
        spider.endTime = time.time()
        longtime=spider.endTime-spider.startTime
        print("程序一共运行了"+str(longtime)+"秒")
        self.fp.close()
