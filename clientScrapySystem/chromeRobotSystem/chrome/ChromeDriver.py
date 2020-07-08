import os
import subprocess
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#谷歌驱动。都存放在这里。当执行这个
class my_diver:

    #启动chrome并且实现接管
    def __init__(self):
        #打开浏览器，并监听窗口，阻塞-+
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")#使用chrome的调试模式
        chrome_driver = "resoure/chromedriver.exe"#用chrome的驱动
        driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

        self.driver=driver
    def get_driver(self):
        return self.driver
if __name__ == '__main__':
  my_diver().get_driver().get('http://001ecchefddflc.jumpbc.chuairan.com/')
  # d.driver.get("https://www.baidu.com")