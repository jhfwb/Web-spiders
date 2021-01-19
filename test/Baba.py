from pydispatch.robustapply import function


class Ni:
    def w1(func:function):
        print(func.__name__)
        print(dir(func))
        def inner1(note):

            print(note)
            # 验证1
            # 验证2
            # 验证3
            func(note)
        return inner1



@Ni.w1
def f1(note="你好"):
    print('f1')
@Ni.w1
def f2():
    print('f2')
@Ni.w1
def f3():
    print('f3')
@Ni.w1
def f4():
    print('f4')
if __name__ == '__main__':
    f1('你好哦')