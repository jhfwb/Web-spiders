# 网络爬虫系统
> 实现商务网站的网络爬虫。

> 该系统分为3个部分。
>1.被爬虫网站的记录与预设
>2.爬虫文件的输出。

## 功能
1. 实现网络爬虫


## 几个核心文件
1. clientScrapySystem/webScrapySystem/GYS_pySpiders/config.xml 用于记录爬虫的地址
记录爬虫规则，记录爬虫文件储存位置
2. 一般我们默认将爬虫的文件储存在Include中。

## 配置文件的配置信息
> 配置文件位置 clientScrapySystem/webScrapySystem/GYS_pySpiders/config.xml 
1. 爬虫信息储存位置:website-dataSave-file(path)
2. 爬虫开始的网址:website(start_url)


## 如何开始程序
1. 运行clientScrapySystem/webScrapySystem/GYS_pySpiders/start.py文件，即可开始爬虫之旅~~

## 开始程序的前提条件
1. 配置config.xml文件，以决定爬虫开始的网址以及位置。