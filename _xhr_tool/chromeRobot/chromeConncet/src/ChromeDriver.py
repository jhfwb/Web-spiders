import socket

from _xhr_tool._annotate import singleObj
from _xhr_tool._utils import relpath
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#谷歌驱动。都存放在这里。当执行这个
from _xhr_tool.chromeRobot.chromeConncet.src.single_chrome_servlet import chrome_browser_open


@singleObj
class ChormeDiver:
    chromeDriverPath = relpath('../resource/chromedriver.exe')
    #启动chrome并且实现接管
    def __init__(self):
        #判断浏览器是否打开，如果没有打开则关闭浏览
        #打开浏览器，并监听窗口，阻塞-+
        # if not self._net_is_used(9222):
        #     chrome_browser_open()
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")#使用chrome的调试模式
        chrome_driver =self.chromeDriverPath#用chrome的驱动
        driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
        self.driver=driver
    def get_driver(self):
        return self.driver

    def _net_is_used(self,port, ip='127.0.0.1'):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            s.shutdown(2)
            print('%s:%d is used' % (ip, port))
            return True
        except:
            print('%s:%d is unused' % (ip, port))
            return False
    def openChrome(self):
        # self.net_is_used(9222)
        chrome_browser_open()
if __name__ == '__main__':

  d=ChormeDiver().get_driver()
  print(d)

  d.close()
  d.quit()
  d.get('https://www.baidu.com/')

  # d.driver.get("https://www.baidu.com")
