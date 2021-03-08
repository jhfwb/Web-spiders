import abc


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