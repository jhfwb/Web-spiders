from clientScrapySystem.chromeRobotSystem.domain.Action import Action


class 搜索百度:
    def run(self):
        # 创建一个机器引擎，

        #机器引擎创建一个Action
        Action().get('https://www.baidu.com/').excute()
        pass