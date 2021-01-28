# class Log:
#     def __init__(self,f):
#         self.f=f
#     def test(self):
#         print('test')
#     def __call__(self, *args, **kwargs):
#         print('before')
#         self.f()
#         print('after')
class Log_class:
    def __init__(self, f):
        pass
    def __call__(self, *args, **kwargs):
        print('运行了')
        pass


def Log(func):
    print('执行了')

# @Log_class
@Log # Log()
def haha():
    print("类装饰器")

if __name__ == '__main__':
    # Log_class('nihao')
    haha.__call__()