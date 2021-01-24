import os

from _xhr_tool._annotate.singleObject import singleObj


@singleObj
class H:
    # def __new__(cls, *args, **kwargs):
    #     pass
    #     print('111')
    #     print(cls)
    #     return super().__new__(cls)
    def __init__(self,a):
        print(a)
    def haha(self):
        print('哈哈')

if __name__ == '__main__':
    print(H(a=1))
    print(H(a=2))


    # H.__new__(cls='')
    # print(H())
