import threading
from queue import Queue

from clientScrapySystem.chromeRobotSystem.src.DataHandle import DataHandle


class MyDataSaveThread(threading.Thread):
    queue = []
    def __init__(self):
        self.dataHandle=DataHandle()
        super().__init__()
        self.queue = Queue()
    def run(self):
        while True:
            item=self.queue.get()
            #保存你的所有信息
            self.dataHandle.catch(item)

