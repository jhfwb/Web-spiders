class ExcuteResponse:
    def __init__(self):
        self.success=None
        self.args={}
        self.errThing={}
    def initResponse(self):
        self.success=None
        self.actName=None
        self.err=None
        self.errType=None
        self.option=None
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
        return str(vars(self))


