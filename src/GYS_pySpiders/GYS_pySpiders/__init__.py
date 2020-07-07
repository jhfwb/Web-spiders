#读取
import os
import re

from src.GYS_pySpiders.Action import Store
from src.GYS_pySpiders.utils.ConfigUtils_spider import SpidersConfigUitls
#读取环境配置
actionConfigUtils=Store.take("actionConfigUtils",SpidersConfigUitls())
spiderNames=[]
for i in range(len(actionConfigUtils.websites)):
    spiderName=actionConfigUtils.websites[i]['webName']
    spiderNames.append(spiderName)

classNames=[]
#先判断item.py文件存在不存在，

if os.path.exists('GYS_pySpiders/items.py'):
    # 读取item.py文件。判断是否已经存在。存在的话就不处理了。
    fp=open(mode='r',file='GYS_pySpiders/items.py',encoding='utf-8')
    itemLines=fp.readlines()
    for itemLine in itemLines:
        if itemLine.find('class')!=-1:
            itemLine=itemLine.replace(' ','')
            className=re.findall(r'class(.*)Item\(scrapy\.Item\):',itemLine)[0]
            classNames.append(className)
    fp.close()


if not classNames==spiderNames:
    #读取模板文件
    fp_template=open(mode='r',file='template/items_template.py',encoding='utf-8')
    lines=fp_template.readlines()
    importLines=[]
    classLines=[]
    for i in range(len(lines)):
        if lines[i].startswith('class '):
            importLines=lines[0:i]
            classLines = lines[i:]
    classLines.append('\n')
    for spiderName in spiderNames:
        for i in range(len(classLines)):

            importLines.append(classLines[i].replace('{{spiderName}}',spiderName))
    #写入该文件。
    pp=open(mode='w',file='GYS_pySpiders/items.py',encoding='utf-8')
    pp.writelines(importLines)
    pp.close()