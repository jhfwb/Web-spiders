import logging
from logging import handlers
class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射
    def __init__(self,savePath="save.log"):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        # 2.1创建一个Handler 用来写入日志文件
        fileHandler = logging.FileHandler(savePath)
        # 2.2创建一个Handler 用来在控制台显示
        streamHandler = logging.StreamHandler()
        # 创建一个
        th = handlers.TimedRotatingFileHandler(filename=savePath, when='D',interval=2, backupCount=3)
        """class logging.handlers.TimedRotatingFileHandler(filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False)
        参数when决定了时间间隔的类型，参数interval决定了多少的时间间隔。如when=‘D’，interval=2，就是指两天的时间间隔，backupCount决定了能留几个日志文件。超过数量就会丢弃掉老的日志文件。
        when的参数决定了时间间隔的类型。两者之间的关系如下："""
        # 3.定义Handler输出的格式
        foramtter = logging.Formatter('%(asctime)s  - %(levelname)s: %(message)s - %(pathname)s[line:%(lineno)d]')
        th.setFormatter(foramtter)
        fileHandler.setFormatter(foramtter)
        streamHandler.setFormatter(foramtter)
        # 4.添加日志消息处理器
        self.logger.addHandler(fileHandler)
        self.logger.addHandler(streamHandler)
        self.logger.addHandler(th)
    def getLogger(self):
        return self.logger
if __name__ == '__main__':
    Logger().logger.info('你好，我是初始信息')