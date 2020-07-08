class Store:
    load={}
    @staticmethod
    def take(key,value):
        """
        核心方法。从load中取出数据，如果该数据不存在则创建一个新数据
        """

        if Store.load.get(key)!=None:
            if value!=Store.load.get(key):

                Store.load[key]=value
                return value
            else:
                return value
        else:
            Store.load.setdefault(key,value)
            return value

    @staticmethod
    def get(key=""):
        return Store.load.get(key)
    @staticmethod
    def set(key,value):
        Store.load.setdefault(key,value)
        return value

if __name__ == '__main__':
    Store.take('afe',213)
    print(Store.take('afe',213))

    # Store.getAttr('name')

