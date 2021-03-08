class ExcuteResponse:
    def __init__(self):
        self.actName = None
        self.success=None
        self.args={}
        self.errThing={}
    def initResponse(self):
        self.setState(actName=None,success=None,
                 errType=None,cssStr=None,datas=None,key_datas=None,index=None,option=None)
        return self
    def setState(self,actName=None,success=None,
                 errType=None,cssStr=None,datas=None,key_datas=None,index=None,option=None):
        self.key_datas = key_datas
        self.datas = datas
        self.success=success
        self.errType = errType
        self.actName = actName
        self.cssStr=cssStr
        self.index=index
        self.option=option

        return self
    def __str__(self):
        obj={}
        for key,value in vars(self).items():
            if value!=None and value!={}:
                obj.setdefault(key,value)
        if len(obj)==0:
            return '{  该excuteResponse未被激活，或者已经被回收  }'
        return str(obj)


