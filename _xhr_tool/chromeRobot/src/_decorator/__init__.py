# 此包用来存放装饰器
#  @chrome_robot_excute 当加上这个方法，则会默认执行有这个方法的文件。
#  @chrome_datas_catch   这相当于一个标志，告诉执行机器人，应当执行保存操作
from _xhr_tool.chromeRobot.src._decorator._decorator import chrome_robot_excute
from _xhr_tool.chromeRobot.src._decorator._decorator import chrome_datas_catch
__all__=['chrome_robot_excute','chrome_datas_catch']

