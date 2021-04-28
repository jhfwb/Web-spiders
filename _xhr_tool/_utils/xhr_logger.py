import logging
from logging import handlers
from _xhr_tool._annotate import singleObj
@singleObj
class Logger(object):
    DEBUG=logging.DEBUG
    INFO=logging.INFO
    WARNING=logging.WARNING
    ERROR=logging.ERROR
    CRITICAL=logging.CRITICAL
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
    def setLevel(self,level=logging.INFO):
        self.logger.setLevel(level)

    def debug(self,message=''):
        return self.logger.debug(message)
    def info(self,message=''):
        return self.logger.info(message)
    def warning(self,message=''):
        return self.logger.warning(message)
if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT)
    d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
    logging.warning('Protocol problem: %s', 'connection reset', extra=d)
    # l=Logger()
    # l.setLevel(level=l.DEBUG)
    # l.logger.debug('你好，我是初始信息')
