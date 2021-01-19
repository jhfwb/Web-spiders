import os
import re
import time

from _xhr_tool._utils.RR_Comments import ChinaWordTool

#索引库
class indexObject:
    def __init__(self):
        self.letterTable=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','OTHERS']
        self.A=0
        self.lines=[]
        self.letterSite={}
    def getDatasByLetter(self,letter=''):#获得字母所在数组。返回一个迭代器。
        datas=self.getDatasAndStatusByLetter(letter=letter)
        if datas==None:
            return None
        return list(map(lambda x:x[0],datas))
    def getDatasAndStatusByLetter(self,letter=''):
        index1 = self.letterSite.get(letter)
        index2 = self.letterSite.get(self._getNextLetter(letter))
        if index1 + 1 == index2:
            return None
        newLines=[]
        for line in self.lines[index1+1:index2]:
            entry=line.split('=')
            key = entry[0].replace('\n','')
            if len(entry)==2:
                value=entry[1].replace('\n','')
            elif len(entry)==1:
                value=None
            else:
                raise ValueError("存在多个等号。有且只允许每行只有一个等号"+line)
            newLines.append((key,value))
        return newLines
    def _getNextLetter(self,letter=""):
        if letter=="OTHERS":
            return None
        for i in range(len(self.letterTable)):
            if self.letterTable[i]==letter:
                return self.letterTable[i+1]
class IndexDatabase:
    def __init__(self,path=""):
        self.path=path
        if not os.path.exists(path):
            fp=open(mode='w',encoding='utf-8',file=path)
            fp.writelines(['IndexDatabase:索引数据库\n','IndexDatabase:'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n',"IndexDatabase:A=3,B=4,C=5,D=6,E=7,F=8,G=9,H=10,I=11,J=12,K=13,L=14,M=15,N=16,O=17,P=18,Q=19,R=20,S=21,T=22,U=23,V=24,W=25,X=26,Y=27,Z=28,OTHERS=29\n",
                           '[A]\n','[B]\n','[C]\n','[D]\n','[E]\n','[F]\n','[G]\n','[H]\n','[I]\n',
                           '[J]\n','[K]\n','[L]\n','[M]\n','[N]\n','[O]\n','[P]\n','[Q]\n','[R]\n',
                           '[S]\n','[T]\n','[U]\n','[V]\n','[W]\n''[X]\n','[Y]\n','[Z]\n','[OTHERS]\n'])

            fp.close()
        needReload = False
        try:
            self.indexObject = self._loadIndexObject()
        except:
            needReload=True
        if needReload==True:
            self._reBuildIndexFile()
        else:
            for key in self.indexObject.letterSite.keys():
                if '['+key+']\n'!=self.indexObject.lines[self.indexObject.letterSite[key]]:
                    needReload=True
                    break
            if needReload:
                self._reBuildIndexFile()
    def _reBuildIndexFile(self):
        datas = []
        # 获取datas
        fp2 = open(mode='r', encoding='utf-8', file=self.path)
        for line in fp2.readlines():
            if not line.startswith('IndexDatabase:') and not line.startswith('['):
                datas.append(line[:len(line) - 1])
        fp2.close()
        try:
            os.rename(self.path, self.path.replace('.txt', '_need_delete.txt'))
        except FileExistsError:
            os.remove(self.path.replace('.txt', '_need_delete.txt'))
            os.rename(self.path, self.path.replace('.txt', '_need_delete.txt'))
        fp = open(mode='w', encoding='utf-8', file=self.path)
        fp.writelines(
            ['IndexDatabase:索引数据库\n', 'IndexDatabase:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n',
             "IndexDatabase:A=3,B=4,C=5,D=6,E=7,F=8,G=9,H=10,I=11,J=12,K=13,L=14,M=15,N=16,O=17,P=18,Q=19,R=20,S=21,T=22,U=23,V=24,W=25,X=26,Y=27,Z=28,OTHERS=29\n",
             '[A]\n', '[B]\n', '[C]\n', '[D]\n', '[E]\n', '[F]\n', '[G]\n', '[H]\n', '[I]\n',
             '[J]\n', '[K]\n', '[L]\n', '[M]\n', '[N]\n', '[O]\n', '[P]\n', '[Q]\n', '[R]\n',
             '[S]\n', '[T]\n', '[U]\n', '[V]\n', '[W]\n''[X]\n', '[Y]\n', '[Z]\n', '[OTHERS]\n'])
        fp.close()
        self.indexObject = self._loadIndexObject()
        for data in datas:
            self.addKeys(data)
    def _saveIndexObjectToFile(self):
        self.indexObject.letterSite
        self.indexObject.lines
    def _updataLetterLines(self):
        line=""
        for key in self.indexObject.letterSite.keys():
            self.indexObject.letterSite[key]
            line+=key+"="+str(self.indexObject.letterSite[key])+","
        line=line[0:len(line)-1]
        self.indexObject.lines[2]="IndexDatabase:"+line+'\n'
    def _loadIndexObject(self):
        """
        根据第三行的数据，载入字母对应表。
        """
        fp = open(mode='r', encoding='utf-8', file=self.path)
        indexObj = indexObject()
        indexObj.lines=fp.readlines()
        fp.close()
        indexObj.letterSite={}
        for entry in indexObj.lines[2][0:len(indexObj.lines[2])-1].replace('IndexDatabase:','').split(','):
            keys=entry.split('=')
            indexObj.letterSite.setdefault(keys[0],int(keys[1]))
        return indexObj
    # def _saveIndexObject(self):
    def isContainKeyName(self,keyName):
        """
        判断是否包含某个索引
        """
        datas=self.indexObject.getDatasByLetter(self._getFirstLetter(keyName))
        if datas==None:
            return False
        return keyName in datas
    def setStatuses(self,keyNames,status):
        for keyName in keyNames:
            self._setSingleStatus(keyName,status)
    def _setSingleStatus(self,keyName,status):
        if not self.isContainKeyName(keyName):
            raise ValueError("不存在该keyName:"+keyName)
        self.deleteKeys(keyName)
        if not status=="":
            self.addKeys(keyName + "=" + str(status))
        else:
            self.addKeys(keyName)
    def _deleteSingleKey(self,keyName):
        """
        删除索引
        """
        if not self.isContainKeyName(keyName):
            raise  ValueError("无法删除数据:keyName。因为,不存在该数据")
        letter=self._getFirstLetter(keyName)
        startIndex=self._getFirstLetterSite(letter)
        deleteInde=-1
        for i in range(startIndex,len(self.indexObject.lines)):
            if self.indexObject.lines[i].split('=')[0].replace('\n','')==keyName:
                deleteInde=i
                break
        deleteData=self.indexObject.lines[i][:len(self.indexObject.lines[i])-1]
        del self.indexObject.lines[deleteInde]
        # 后移所有数据
        removeSign = 0
        for key in self.indexObject.letterSite.keys():
            if removeSign == 1:
                self.indexObject.letterSite[key] = self.indexObject.letterSite[key] - 1  # 后期可以改成多个
            if key == letter:
                removeSign = 1
        return deleteData
    def deleteKeys(self,keyNames):
        if type(keyNames) == type(""):
            keyNames = [keyNames]
        if type(keyNames) != type([]):
            raise ValueError("KeyName必须是list类型," + str(keyNames) + "不是list类型")
        deleteDatas=[]
        for keyName in keyNames:
            deleteData=self._deleteSingleKey(keyName)
            if deleteData!=None:
                deleteDatas.append(deleteData)
        self._updataLetterLines()
        fp = open(mode='w', encoding='utf-8', file=self.path)
        self.indexObject.lines[1] = 'IndexDatabase:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
        fp.writelines(self.indexObject.lines)
        fp.close()
        return deleteDatas
    def _getFirstLetterSite(self,letter):
        """
        获得首个字母在line中的位置
        """
        return self.indexObject.letterSite.get(letter)

    def getKeyNamesByLetters(self,letter="A"):
        """
        e.g:getKeyNamesByLetters(letter="A")
        获得所有以A为首拼音的数据集合
        @param letter |str letter的可选参数：A,B,C.....X,Y,Z,OHTERS (务必注意必须是大写)
        """
        return self.indexObject.getDatasByLetter(letter)

    def getKeyNamesAndStatusByLetters(self, letter="A"):
        """
        e.g:getKeyNamesByLetters(letter="A")
        获得所有以A为首拼音的数据集合
        @param letter |str letter的可选参数：A,B,C.....X,Y,Z,OHTERS (务必注意必须是大写)
        """
        return self.indexObject.getDatasAndStatusByLetter(letter)
    def getAllKeyNamesAndStatus(self):
        datas = []
        for letter in self.indexObject.letterTable:
            letterDatas = self.getKeyNamesAndStatusByLetters(letter)
            if letterDatas != None:
                datas = datas + letterDatas
        return datas
    def getAllKeyNames(self):#???????
        """
        获得所有索引
        """
        datas = []
        for letter in self.indexObject.letterTable:
            letterDatas = self.getKeyNamesByLetters(letter)
            if letterDatas != None:
                datas = datas + letterDatas
        return datas
    def getStatusByKeyNames(self,keyName):
        """
        获得关键字的状态。
        """
        if self.isContainKeyName(keyName):
            items=self.getKeyNamesAndStatusByLetters(self._getFirstLetter(keyName))
            for item  in items:
                if item[0]==keyName:
                    return item[1]
        else:
            raise ValueError('keyName:'+keyName+'不存在')
    def addKeys(self,keyNames,status=""):
        """
        添加索引。如果成功添加，则会返回该keyNames数组。当然，如果keyNames只有一个数据，则只会返回一个数据
        如果添加失败。则会返回None

        """
        if keyNames=="":
            return
        if type(keyNames) == type(""):
            keyNames = [keyNames]
        if type(keyNames) != type([]):
            raise ValueError("KeyName必须是list类型," + str(keyNames) + "不是list类型")
        bos=[]
        for keyName in keyNames:

            bo=self._addSingleKey(keyName,status)
            if bo:
                bos.append(keyName)
        if len(bos)>0:
            self._updataLetterLines()
            fp = open(mode='w', encoding='utf-8', file=self.path)
            self.indexObject.lines[1]='IndexDatabase:'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n'
            fp.writelines(self.indexObject.lines)
            fp.close()
            return bos
        else:
            return None#
    def _getFirstLetter(self,keyName):
        letter = ChinaWordTool.getStrFirstAplha(keyName)  # 获得首字母
        try:
            re.match(r'[A-Z]', letter).group()
        except:
            letter = 'OTHERS'
        return letter
    def _addSingleKey(self,keyName,status=""):
        if self.isContainKeyName(keyName):
            return False
        if '\n' in keyName:
            raise ValueError("KeyName不可以包含\\n")
        if keyName==None:
            raise ValueError("KeyName不可以是None")
        if keyName=="":
            raise ValueError("KeyName的长度不可以为0")
        if type(keyName)!=type(""):
            raise ValueError("KeyName必须是字符串类型,"+str(keyName)+"不是字符串类型")
        if str(status)!="":
            keyName=keyName+'='+str(status)
        letter=self._getFirstLetter(keyName)
        letterDataArr=self.indexObject.getDatasByLetter(letter)#获得该字母对应的数组
        if letterDataArr==None:
            letterDataArr=[]
        sign=1
        for letterData in letterDataArr:
            if keyName+'\n'==letterData:
                sign=0
        if sign==1:
            self.indexObject.lines.insert(self._getFirstLetterSite(letter)+1,keyName+'\n')
            #后移所有数据
            addSign=0
            for key in self.indexObject.letterSite.keys():
                if addSign==1:
                    self.indexObject.letterSite[key] = self.indexObject.letterSite[key]+1#后期可以改成多个
                if key==letter:
                    addSign=1
        return True

if __name__ == '__main__':
    # arr=[1,2,3]
    # arr.insert(2,233)
    # print(arr)
    a=IndexDatabase(
        '/clientScrapySystem/DatabaseSystem/database/indexData.txt')
    # a.addKeys(['我1','我2'],-1)
    # a.addKeys('你好1')
    # a.addKeys('你好2','132132112321')
    c=a.addKeys(['你好23211','21321'])
    print(c)
    print(a.getAllKeyNamesAndStatus())
