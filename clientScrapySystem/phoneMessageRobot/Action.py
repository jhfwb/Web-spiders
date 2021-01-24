from _xhr_tool._utils.CsvTool import CsvTool
from clientScrapySystem.phoneMessageRobot.dataHandle.engine.DataHandle import DataHandle


class Action:
    """
    用于发送短信的环境
    """
    def __init__(self):
        # adb='adb devices'
        # os.system(adb)
        # 读取数据库数据
        # datas=CsvTool().optionCsv(path='test.csv',mode='r')
        # fpRead = open(mode='r', file='sendedPhone/sendedPhone.txt')
        # readedPhones = fpRead.readlines()
        # fpRead.close()
        # fpWriter = open(mode='a', file='sendedPhone/sendedPhone.txt')
        # tool.print("运行cmd代码:正在连接手机中...", fontColor='blue')
        # 1.处理数据,并获得数据集。
        DataHandle().dataHandle(filePath='dataHandle/test_2.csv')
        # 2.获得待发送数据。
        data()=CsvTool().popLastData(path='test.csv', isPop=False)

        """
        1. 从数据中取出末尾数据
        2. 发送数据
            成功:在仓库中取出数据
            失败:不取出数据
        3. 
        """
        # 出一个数据，保存一个数据

        # # #循环执行脚本
        # robot = Robot()
        # # for data in datas:
        # for data in datas:
        #     # 从电话库中取出电话。判断该电话是否有被发送过
        #     fp = open(mode='r', file='sendedPhone/sendedPhone.txt')
        #     readedPhones = fp.readlines()
        #     fp.close()
        #     if not data['phone'] + '\n' in readedPhones:
        #         robot.editMessage(data['phone'], data['message'], openPrint=True, isTest=True)
        #         tool.print("成功发送以下短信:" + data['message'], fontColor='pink')
        #         fpWriter.write(data['phone'] + '\n')
        #         fpWriter.flush()
        # fpWriter.close()