import abc
class ExcuteEngine_abstract(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self):
        pass
    @abc.abstractmethod
    def start(self):
        pass
    @abc.abstractmethod
    def close(self):
        pass

class ObjsPool_abstract(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        pass
    @abc.abstractmethod
    def get(self):
        pass
    @abc.abstractmethod
    def back(self):
        pass