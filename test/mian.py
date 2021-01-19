
def foo(*args, **kwargs):
    print('args =', args)
    print('kwargs = ', kwargs)

if __name__ == '__main__':
    foo(3,a=1,b=2)
    a={}
    print(a.get('note'))

