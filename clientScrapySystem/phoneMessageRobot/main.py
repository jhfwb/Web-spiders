from clientScrapySystem.phoneMessageRobot.Action import Action

# 分别对三个文件进行简单介绍
# midData.csv 对发送的数据进行初级处理的地方。可以用表达式等。如果为空，则继承上一条数据的值
# checkData.csv 检查数据的地方。为了避免数据发生错误，会生成checkdata.csv。用于给我们检查
# 之后发送短信的时候，会用到message与phone。因此一定要有这两个值

if __name__ == '__main__':
    Action()


