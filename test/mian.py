import os

from test.你好.haha import haha

if __name__ == '__main__':
    print(1)
    haha
    print(os.getcwd())
    os.chdir("C:/Users/1234567/Desktop/git库存储/Web-spiders")
    print(os.getcwd())
    print(os.path.exists('test/你好/test'))
    #
    # print(os.getcwd())
    # print(os.path.exists('你好/test'))
    # print(dir)
