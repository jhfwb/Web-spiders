
def log(func):
    """
    在方法前加上@log
    当拥有该注解的方法，拥有以下特性。
    当该方法的参数有note的时候，则会在屏幕中打印note
    """
    def log1(*args, **kwargs):
        print('装饰了!')
        func(*args, **kwargs)
    return log1 # 返回需要执行的新的方法
@log
def test(s):
    print('我是'+s+'方法')
if __name__ == '__main__':
    test('测试')
