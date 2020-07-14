from clientScrapySystem.chromeRobotSystem.chrome.ChromeDriver import my_diver
from clientScrapySystem.chromeRobotSystem.servlet.pipeline_thread import MyDataSaveThread
from clientScrapySystem.chromeRobotSystem.servlet.robot_thread import MyPipelineThread
from clientScrapySystem.chromeRobotSystem.天眼查 import 天眼查

class Context:
    def __init__(self):
        driver = my_diver().get_driver()  # 打开接管浏览器
        # 注册机器人线程
        self.robotThread = MyPipelineThread(driver)
        self.robotThread.context=self
        # 注册管道线程
        self.saveThread = MyDataSaveThread(driver)
        self.saveThread.context=self
        #后期要改
        # robot2 = 天眼查()
        # robot2.run(self.robotThread)
        # pass

    def main(self):
        self.robotThread.start()
        self.saveThread.start()
        pass

    pass
if __name__ == '__main__':
    Context().main()





