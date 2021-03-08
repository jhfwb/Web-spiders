import logging
# 1.创建日志对象
logger=logging.getLogger()

loggera=logging.getLogger('myselflogging')    #w
loggera.setLevel(logging.DEBUG)

loggerb=logging.getLogger('myselflogging')
loggerb.setLevel(logging.INFO)

loggerc=logging.getLogger('myselflogging.a')
loggerc.setLevel(logging.WARNING   )

loggerd=logging.getLogger('myselflogging.a.a')
loggerd.setLevel(logging.ERROR)

loggere=logging.getLogger('myselflogging.a.a.a')
loggere.setLevel(logging.CRITICAL)

# 2.1创建一个Handler 用来写入日志文件
fobj=logging.FileHandler('FileHandler.log')
# 2.2创建一个Handler 用来在控制台显示
sobj=logging.StreamHandler()
# 3.定义Handler输出的格式
foramtter=logging.Formatter('%(asctime)s  - %(levelname)s: %(message)s - %(pathname)s[line:%(lineno)d]')
fobj.setFormatter(foramtter)
sobj.setFormatter(foramtter)
# 4.添加日志消息处理器
logger.addHandler(fobj)
logger.addHandler(sobj)

#日志输出
print('未显示设定日志等级，默认为Warning')
logger.debug('logger debug message')
logger.info('logger info message')
logger.warning('logger warning message')
logger.error('logger error message')
logger.critical('logger critical message')

print('loggera=myselflogging，显示设定等级是：logging.DEBUG')
loggera.debug('loggera debug message')
loggera.info('loggera info message')
loggera.warning('loggera warning message')
loggera.error('loggera error message')
loggera.critical('loggera critical message')

print('loggerb=myselflogging，显示设定等级是：logging.INFO')
loggerb.debug('loggerb debug message')
loggerb.info('loggerb info message')
loggerb.warning('loggerb warning message')
loggerb.error('loggerb error message')
loggerb.critical('loggerb critical message')

print('loggerc=myselflogging，显示设定等级是：logging.WARNING')
loggerc.debug('loggerc debug message')
loggerc.info('loggerc info message')
loggerc.warning('loggerc warning message')
loggerc.error('loggerc error message')
loggerc.critical('loggerc critical message')

print('loggerd=myselflogging，显示设定等级是：logging.ERROR')
loggerd.debug('loggerd debug message')
loggerd.info('loggerd info message')
loggerd.warning('loggerd warning message')
loggerd.error('loggerd error message')
loggerd.critical('loggerd critical message')

print('loggere=myselflogging，显示设定等级是：logging.CRITICAL')
loggere.debug('loggere debug message')
loggere.info('loggere info message')
loggere.warning('loggere warning message')
loggere.error('loggere error message')
loggere.critical('loggere critical message')