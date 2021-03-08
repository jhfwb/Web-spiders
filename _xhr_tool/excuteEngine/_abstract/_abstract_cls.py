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
class Interceptor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def excute_before(self):
        pass
    @abc.abstractmethod
    def excute_after(self):
        pass
