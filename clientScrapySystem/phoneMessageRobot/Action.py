from _xhr_tool import Device
from _xhr_tool._utils.CsvTool import CsvTool
from clientScrapySystem.phoneMessageRobot.dataHandle.DataHandle import DataHandle


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
        datas = DataHandle().dataHandle(inputPath='dataHandle/handleDatas/test.csv', keys=['phone', 'message'], idkey='phone',
                             outputPath='dataHandle/handleDatas/send.csv')
        # 1.加载csv文件，获得已发送短信的集合。
        sendedDatas = CsvTool().optionCsv(path='dataHandle/disk/sendedPhone.csv', mode='r', isCreateFile=True)
        print(sendedDatas)
        # 2.加载csv文件，获得需要发送的短信集合。
        print(datas)

        # 3.筛选，去掉重复的数据。获得待发送数据。将该数据保存起来。






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