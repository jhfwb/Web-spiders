from selenium.webdriver.common.keys import Keys
from clientScrapySystem.chromeRobotSystem.domain.Action import Action


class 天眼查:
    #此处放入地址库
    def __init__(self):
        pass
    def run(self,myThread):
        #1.读取excel数据文档。获取到公司的名称。
        #2.访问百度。读取公司信息，保存快照
        #3.访问天眼查。读取公司信息，保存天眼查的公司名称，以及公司的所有电话，主营产品，（建议保存在单独的文本文件中）
        #创建洞丛
        #读取公司信息。将数据循环到处
        # exceTool=ExcelTool()
        # exceTool.optionExecl(path='',mode='r')
        def exception(action):
            action.find(cssStr="div.f0 span:nth-child(2)", key="电话")
        def success(action):
            action.find(cssStr=".phone-item .phone", key="电话", mode="multiple").\
            click(cssStr=".modal-dialog .close")
        Action("天眼查搜寻公司信息。").initWeb().\
            get("https://www.tianyancha.com/?jsid=SEM-BAIDU-PZ2006-SY-000001").\
            key_input(cssStr="[type='search']",text="福建省邦消消防科技有限公司",isClear=True).\
            key_input(cssStr="[type='search']",text=Keys.ENTER,isClear=False).\
            click(cssStr="div.result-list.sv-search-container > div:nth-child(1) a.name").\
            find(cssStr=".name",key="公司名"). \
            find(cssStr=".summary", key="公司简介"). \
            find(cssStr="table.-striped-col.-border-top-none.-breakall", key="公司信息"). \
            click(cssStr="span.link-click.link-spacing",exception=exception,success=success).\
            excute(myThread.readyExcute)
        # myThread.queue.put({'way': 'init'})#初始化
        # myThread.queue.put({'way':'get',
        #                     "text":"https://www.tianyancha.com/?jsid=SEM-BAIDU-PZ2006-SY-000001",
        #                     })
        #
        # myThread.queue.put({'way': 'key_input',
        #                     "css":"[type='search']",
        #                     "text": "武安市武安镇喝喝哈哈商品经销部",
        #                     "isClear":True})
        # myThread.queue.put({'way': 'key_input',
        #                     "css": "[type='search']",
        #                     "text": Keys.ENTER,
        #                     "isClear": False})

        # myThread.queue.put({'way': 'click',
        #                     "css": "div.result-list.sv-search-container > div:nth-child(1) a.name",
        #                     })#点击列表第一个
        #
        # myThread.queue.put({'way': 'click',
        #                     "css": "span.link-click.link-spacing",
        #                     "memo":"点击查看电话"
        #                     })  # 点击查看电话
        #
        # myThread.queue.put({'way': 'find',
        #                     "css": "div.body.-scorll-fix.-phone.modal-scroll",
        #                     "key":"电话",
        #                     "memo": "爬取电话"
        #                     })  # 点击查看更多

        # myThread.queue.put({'way': 'screenshot',#找到上网页上的单个信息，获得网页快照，获得
        #                     'path':'D:/编程/workpathByPython/chromeRobotSystem/福建天广消防科技有限公司.png'
        #                     })
        # myThread.queue.put({'way': 'find',  # 找到上网页上的单个信息，获得网页快照，获得
        #                     'dataCatchBySelector':{'name':'选择器1','age':'选择器2'},
        #                     'saveWay': 'D:/编程/workpathByPython/chromeRobotSystem/福建天广消防科技有限公司.png'#第一种是保存到csv或者excel中。第二种就是保存到记事本中
        #                     })#最终会返回一个对象这个对象包含，name，age属性，甚至包含_url的属性


        # myThread.queue.put({'way': 'screenshot',  # 找到上网页上的单个信息，获得网页快照，获得
        #                     'path': 'D:/编程/workpathByPython/chromeRobotSystem/111.png'
        #                     })
        # myThread.queue.put({'way': 'close'})
        # driver.save_screenshot("xxx.png")


