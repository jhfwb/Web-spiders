#encoding=utf8
#http://www.fanjun.me/?p=568
def test(func):
    def run(*args,**kwargs):
        func(*args,**kwargs)
    return run
@test
def xixi(aa,a=1,b=2,c=3):
    aa=locals()
    b=__name__
    tongyong()
    pass
def tongyong():
    nonlocal aa
    option = vars()
    print(aa)
    option.setdefault('way',)
    print('运行关键代码')
    pass
if __name__ == '__main__':
    xixi(12212)

