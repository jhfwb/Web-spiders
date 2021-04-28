class A:
    name='张三'
    def __init__(self):
        self.age=1
    pass
if __name__ == '__main__':
    a=A()
    b=A()
    A.name='力达'
    print(a.age)
    print(b.age)

# def test(a=1,b=2):
#     print(a)


    # a=ReflexTool.getMethod(filePath="C:\\Users\\1234567\\Desktop\\git库存储\\Web-spiders\\Lib\\test.py",className='haha',methodName='b')
    # a=ReflexTool.newInstance(filePath="C:\\Users\\1234567\\Desktop\\git库存储\\Web-spiders\\Lib\\test.py",className='haha',options={'a':222})
    # print(a)
    # print(test.haha)

    # sys.path.append("C:/Users/1234567/Desktop/git库存储/Web-spiders/_utils")
    # print(sys.path)
    # exec('import "C:/Users/1234567/Desktop/git库存储/Web-spiders/_utils"')
    # # print(PrintTool)
    # ReflexTool.execute(function=PrintTool.print,options={'s':"Nihao"})
