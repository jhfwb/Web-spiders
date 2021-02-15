import inspect
import threading
import sys
from _xhr_tool._annotate import threadingRun, singleObj
class ReflexUtils:
    """最好不要使用单例模式，否则会对服务器造成负担"""
    def __init__(self):
        pass
    def excuteAllDecorator(self, obj={}, decoratorName="", args=[]):
        funcs = self.getFuncByDecoratorName(className=obj.__class__, decoratorName=decoratorName)
        results=None
        for func in funcs:
            results = func(obj, *args)
        return results
    def excuteDecorator(self,obj={},decoratorName="",args=[]):
        func=self.getFuncByDecoratorName(className=obj.__class__,decoratorName=decoratorName)[0]
        try:
            result=func(obj,*args)
        except TypeError:
            raise SyntaxError('语法错误:该类:' + str(obj.__class__) + ':的方法中缺少' + decoratorName + '注解,无法指'
                                                                                                     '定执行' + decoratorName + '下的方法。建议在该类中创建一个方法，该方法需要被装饰器' + decoratorName + '注解')
        return result
    def _removeNotes(self,s):
        """
        去除掉字符串中的注解
        e.g:
            s='
            @threadingRun # 我是注解
            def haha(self,s,dd):
                print('你好'+s)
                 # 我是注解
            '
            去除后:
            s='
            @threadingRun
            def haha(self,s,dd):
                print('你好'+s)
            '
        :param s: 字符串
        :return:
        """
        arr=s.split('\n')
        notes=[]
        for i in range(len(arr)):
            startInt=arr[i].find('#')
            if startInt!=-1:
                arr[i]=arr[i][0:startInt]
        s="\n".join(arr)
        return s
    def getFuncByDecoratorName(self,className,decoratorName=""):
        """
        根据装饰器名称，获得被该装饰器修饰的方法。
        注意！由于该方法内部使用到inspect.getsource()。为了避免装饰器修改了类。因此需要在方法中添加
        """

        try:
            if hasattr(self,'_'+str(className)+'_src'):
                pass
            else:
                # 将注释去除掉
                s=inspect.getsource(className)
                s=self._removeNotes(s)
                setattr(self, '_'+str(className) + '_src',s)
            s=getattr(self,'_'+str(className)+'_src')
        except TypeError:
            raise TypeError('类型错误:'+str(className)+"必须是类对象")
        arr=[]
        _index=0
        while(_index!=-1):
            _index=s.find(decoratorName,_index+1)
            if _index==-1:
                break
            defIndex_start=s.find('def',_index)+3
            defIndex_end=s.find('(',defIndex_start)
            line=s[defIndex_start:defIndex_end].strip()
            arr.append(getattr(className, line))
        return arr
class A:
    @threadingRun
    def haha(self,s,dd):
        print('你好'+s)
    @threadingRun
    def haha2(self):
        print('你好')

if __name__ == '__main__':
    print(ReflexUtils().getFuncByDecoratorName(A,'@threadingRun'))
    # print(ReflexUtils().getFuncByDecoratorName(A(),'@threadingRun','我不好','woow'))