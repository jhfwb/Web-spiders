from selenium.webdriver.common.keys import Keys


class add_address_4life:
    #此处放入地址库
    def __init__(self):
        pass
    def run(self,myThread):
        #1.读取excel数据文档。获取到公司的名称。
        #2.访问百度。读取公司信息，保存快照
        #3.访问天眼查。读取公司信息，保存天眼查的公司名称，以及公司的所有电话，主营产品，（建议保存在单独的文本文件中）
        myThread.queue.put({'way': 'init'})#初始化
        myThread.queue.put({'way':'get',
                            "text":"https://www.baidu.com"})
        myThread.queue.put({'way': 'key_input',
                            "css":"#kw",
                            "text": "福建天广消防科技有限公司",
                            "isClear":True})
        myThread.queue.put({'way': 'key_input',
                            "css": "#kw",
                            "text": Keys.ENTER,
                            "isClear": False})
        myThread.queue.put({'way': 'click',
                            "css": "[id='1'] a",})
        myThread.queue.put({'way': 'screenshot',#找到上网页上的单个信息，获得网页快照，获得
                            'path':'D:/编程/workpathByPython/chromeRobotSystem/福建天广消防科技有限公司.png'})
        # myThread.queue.put({'way': 'find',  # 找到上网页上的单个信息，获得网页快照，获得
        #                     'dataCatchBySelector':{'name':'选择器1','age':'选择器2'},
        #                     'saveWay': 'D:/编程/workpathByPython/chromeRobotSystem/福建天广消防科技有限公司.png'#第一种是保存到csv或者excel中。第二种就是保存到记事本中
        #                     })#最终会返回一个对象这个对象包含，name，age属性，甚至包含_url的属性
        # myThread.queue.put({'way': 'screenshot',  # 找到上网页上的单个信息，获得网页快照，获得
        #                     'path': 'D:/编程/workpathByPython/chromeRobotSystem/111.png'
        #                     })
        myThread.queue.put({'way': 'close'})
        # driver.save_screenshot("xxx.png")


