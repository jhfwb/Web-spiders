# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
# 判断是否config.xml中需要被执行的spider是否存在，如果不存在则在template文件夹下面的的spider_template.py为模板创建，一个新
# 的spider。名字按照name命名
"""
根据配置文件中的爬虫项目，动态创建爬虫。根据模板创建（template/spider_template.py）。创建在本文件夹下面。
"""
import re
from src.GYS_pySpiders.Action import Store
from src.GYS_pySpiders.utils.ConfigUtils_spider import SpidersConfigUitls
import os
#获取其初始化配置文件(如果没有，则创建一个新的配置文件)
actionConfigUtils=Store.take("actionConfigUtils",SpidersConfigUitls())
#获取当前目录下(spider文件)所有的文件的工作路径。并保存在filePaths这个数组中 e.g['GYS_pySpiders/spiders/Spider_招商100.py', 'GYS_pySpiders/spiders/Spider_顺企网.py', 'GYS_pySpiders/spiders/__init__.py']
filePaths=[]
#获取当前目录下(spider文件)所有spider的name属性名 e.g:['招商100', '顺企网']
spiderNameFiles = []
for root, dirs, files in os.walk("GYS_pySpiders/spiders"):
    filePaths=list(map(lambda x:root+'/'+x,files))
    break
#读取spider文件下面所有spider文件（除了_init_.py文件）。并通过os流读取其spider的名称。并保存在spiderNameFiles数组中
for filePath in filePaths:
    files=open(mode='r',file=filePath,encoding='utf-8')
    lines=files.readlines()
        #存放了所有spider的名称
    for line in lines:
        if line.find('name')!=-1:
            newLine=line.strip().replace(' ','')
            if newLine.startswith("name="):
                spiderNameFiles.append(re.findall(r'\'(.*)\'',newLine)[0])
                break
    files.close()##
# 通过对比spiderNameFiles(上面有)与从配置文件config.xml中的webName。得到一个数组:creatFies。用来之后创建新的.py文件
creatFies=[]
for i in range(len(actionConfigUtils.execs)):
    spiderName=actionConfigUtils.execs[i]['webName']
    if not spiderName in spiderNameFiles:
        #根据模板创建一个新的py对象。
        creatFies.append(spiderName)
    #检索这个包里面有没有name为spiderName的蜘蛛
if not len(creatFies)==0:
    createFilesLinses=[]
    #提取模板
    fp=open(mode='r',file='template/spider_template.py',encoding='utf-8')
    templateLines=fp.readlines()
    print(len(creatFies))
    for creatFie in creatFies:
        createFilesLinses.append((creatFie,templateLines.copy()))

    for i in range(len(templateLines)):
        if templateLines[i].find('{{spiderName}}')!=-1:
            for j in range(len(createFilesLinses)):
                createFilesLinses[j][1][i]=templateLines[i].replace('{{spiderName}}',createFilesLinses[j][0])
    fp.close()
    #写入文档
    for name,lines in createFilesLinses:
        fp=open(mode='w',file='GYS_pySpiders/spiders/Spider_'+name+'.py',encoding='utf-8')

        fp.writelines(lines)
        fp.close()
