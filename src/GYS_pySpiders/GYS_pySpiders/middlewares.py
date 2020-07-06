# -*- coding: utf-8 -*-
# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import csv
from scrapy import signals

from src.GYS_pySpiders.utils.RR_Comments import PrintTool


class GysPyspidersSpiderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        # 读取配置。
        s = cls()  # s是这个中间键的一个实例对象。cls是GysPyspidersSpiderMiddleware这个类。
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s
    def process_spider_input(self, response, spider):

        return None
    def process_spider_output(self, response, result, spider):

        for i in result:
            yield i
    def process_spider_exception(self, response, exception, spider):
        pass
    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r
    def spider_opened(self, spider):

        # 爬虫机器人开始的时候，
        spider.logger.info('Spider opened: %s' % spider.name)
class GysPyspidersDownloaderMiddleware(object):
    scrapy_urls = []
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s
    def process_request(self, request, spider):
        # PrintTool.print("1_process_request！！！！"+spider.name, fontColor='pink')
        if len(self.scrapy_urls) != 0:
            for scrapy_url in self.scrapy_urls:
                if scrapy_url == request.url:
                    # self.scrapy_urls.remove(scrapy_url)
                    # print("这条爬虫是重复的！！！！！！！！！！！！！！！！")
                    # print(len(self.scrapy_urls))
                    return request
                else:
                    pass
        return None
    def process_response(self, request, response, spider):
        # PrintTool.print("2_process_response！！！！" + spider.name, fontColor='pink')
        return response
    def process_exception(self, request, exception, spider):

        pass
    def spider_opened(self, spider):
        """
        当次spider打开的时候运行
        """
        # PrintTool.print("spider_opened！！！！" + spider.name, fontColor='pink')
        fileName = spider.fileName
        unicode = spider.unicode
        fp=open(fileName, 'r', encoding=unicode)
        # encoding是读取时候的解码规则
        reader = csv.DictReader(fp)
        # print(map(lambda entry:entry['信息获取的来源url'],list(reader)))
        global scrapy_urls
        self.scrapy_urls = list(map(lambda entry: entry['_url'], list(reader)))
        fp.close()
