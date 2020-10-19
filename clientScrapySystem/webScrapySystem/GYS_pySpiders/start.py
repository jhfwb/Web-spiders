import re
import threading

from scrapy.cmdline import execute
#改变配置文件
#取出配置文件中的{{}}
#读取配置文件
# obj={'keyName':[]}
#
# file=open(file='config.xml',mode='r',encoding='utf-8')
# lines=file.readli           nes()
# for line in lines:
#     re.sub(r'\{\{.*\}\}',line)
# print(lines)
# assert 1/0
# 运行cmd代码，运行爬虫文件
execute("scrapy crawlall".split())

# execute(['scrapy', 'crawl', '_pySpider'])
# print('23333')
# execute("scrapy crawlall".split())
# execute(['scrapy', 'crawl', '_pySpider'])


