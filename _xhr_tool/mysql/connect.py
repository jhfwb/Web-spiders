import pymysql

from _xhr_tool._annotate import singleObj


class Condition:
    def __init__(self,key,value):
        return key+'='+value
class MySqlOptions:
    """
    1.查询
    2.插入
    """
    def __init__(self,host='localhost', user='root', password='512124632', database='crapydatabase'):
        self.conn = pymysql.connect(host=host, user=user, password=password, database=database)
        self.cur = self.conn.cursor()
    def _handleObj(self,objDict={}):
        """
        处理字典集，将
        :param objDict:
        :return:
        """
        newObj={}
        for key,item in objDict.items():
          if item!=None:
              newObj.setdefault(key,item)
        return newObj

    def find_tables(self,table='',joinConditions=[],columns=[],conditions=[], sort='', limit=1, ):
        """
        option.find_tables(table='messages',joinConditions=[('customers',('客户id','id')),],columns=[])
        :param table:
        :param joinConditions:[('tableName1',(主表属性,从表属性),...),('tableName2',(主表属性,从表属性),...)]
        :param columns:
        :param conditions:
        :param sort:
        :param limit:
        :return:
        """
        if len(columns)==0:
            columnsStr='*'
        else:
            columnsStr = ",".join(map(lambda x: '`' + x + '`', columns))
        try:
            conditionsStr = " AND ".join(
                map(lambda x: str('`' + x[0] + '`') + '=' + '\'' + str(x[1]) + '\'', conditions))
        except IndexError:
            raise ValueError('conditions参数异常：请确保如下方式进行__conditions=[(id,1),(name=张三)]')
        if columnsStr == "":
            raise ZeroDivisionError("columnS参数为空,请务必赋值")
        sql_where = ""
        if conditionsStr.strip() != "":
            sql_where = "WHERE " + conditionsStr
        joinStr=""
        if len(joinConditions)!=0:
            for joinCondition in joinConditions:
                joinStr+='JOIN `'+joinCondition[0]+'`'
                joinc=""
                for join in joinCondition[1:]:
                    joinc+='`'+table+'`.'+join[0]+'=`'+joinCondition[0]+'`.'+join[1]+' AND '
                if joinc!='':
                    joinc=' ON '+joinc[0:len(joinc)-5]+'\n'
                joinStr+=joinc
            joinStr=joinStr[0:len(joinStr)-1]
        sql = """
SELECT """ + columnsStr + """ 
FROM `""" + table + """`
"""+joinStr+"""
""" + sql_where + """;
"""
        try:
            self.cur.execute(sql)
            return (self._getColumesName(),)+self.cur.fetchall()
        except pymysql.err.OperationalError as a:
            print('\033[31m-----异常sql语句------' + sql)
            raise a
    def _getColumesName(self):
        arr=[]
        for ee in self.cur.description:
            arr.append(ee[0])
        return tuple(arr)
    def find(self,table='',columns=[],conditions=[],joinCondition=[],sort='',limit=1,):
        columnsStr=",".join(map(lambda x:'`'+x+'`',columns))
        try:
            conditionsStr=" AND ".join(map(lambda x:str('`'+x[0]+'`')+'='+'\''+str(x[1])+'\'',conditions))
        except IndexError:
            raise ValueError('conditions参数异常：请确保如下方式进行__conditions=[(id,1),(name=张三)]')
        if columnsStr=="":
            raise ZeroDivisionError("columnS参数为空,请务必赋值")
        sql_where=""
        if conditionsStr.strip()!="":
            sql_where="WHERE "+conditionsStr
        sql="""
SELECT """+columnsStr+""" 
FROM `"""+table+"""`
"""+sql_where+""";
"""
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except pymysql.err.OperationalError as a:
            print('\033[31m-----异常sql语句------'+sql)
            raise a
    def findAll(self,table='',conditions=[],):
        pass
    def insert(self,table='',objDict={}):
        #1.获取头
        objDict=self._handleObj(objDict)
        if len(objDict)==0:
            raise ZeroDivisionError('添加的数据为空，参数objDict长度为0:'+str(objDict))
        keys=str(list(objDict.keys()))
        keys=keys[1:len(keys)-1].replace('\'','`').replace('\"','`')
        value=str(list(objDict.values()))
        value = value[1:len(value) - 1]
        sql="""INSERT INTO """+table+"""("""+keys+""")
VALUE ("""+value+""");
"""
        try:
            self.cur.execute(query=sql)
            self.conn.commit()
            return True
        except pymysql.err.ProgrammingError as ee:
            print(ee)
            return False
        except pymysql.err.OperationalError  as ee:
            print(ee)
            return False
        except pymysql.err.IntegrityError as ee:
            print(ee)
            return False
        except pymysql.err.DataError as ee:
            print(ee)
            return False
    def getTableDict(self,table=''):
        """
        获得表格的字典
        :param table:
        :return:
        """
        self.cur.execute(query='DESC '+table+';')
        # self.conn.commit()
        obj={}
        _tups=self.cur.fetchall()
        for tup in _tups:
            obj.setdefault(tup[0],None)
        return obj
    def excuteSql(self,sql=""):
        a=self.cur.execute(sql)
        return self.cur.fetchall()
    #读取表的所有字段，并保存成值

    # def search(self,table='',objDict={},condition=''):
    def update(self,table='',columeName='',newValue='',conditions=[]):
        try:
            conditionsStr=" AND ".join(map(lambda x:str('`'+x[0]+'`')+'='+'\''+str(x[1])+'\'',conditions))
        except IndexError:
            raise ValueError('conditions参数异常:请确保如下方式进行__conditions=[(id,1),(name=张三)]')
        sql_where = ""
        if conditionsStr.strip() != "":
            sql_where = "WHERE " + conditionsStr

        sql = """
UPDATE """ + table + """ 
SET """ + columeName +"""="""+str(newValue)+"""
""" + sql_where + """;
"""
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except pymysql.err.OperationalError as a:
            print('\033[31m-----异常sql语句------' + sql)
            self.conn.rollback()
            print("更新失败")
            raise a

if __name__ == '__main__':
    # 创建一个工具，专门用于定义:
    # 表的名称，属性，
    option=MySqlOptions()
#     a=option.excuteSql(sql=
# """
# SELECT *
# FROM messages
# WHERE id=1;""")
#     print(a)
#     a=option.find(table='messages',columns=['id','信息'],conditions=[('id',1)])
    a=option.find_tables(table='messages',joinConditions=[('customers',('客户id','id')),],columns=[])
    # a=option.update(table='messages',columeName='客户id',newValue=6,conditions=[('id',1)])
    print(a)
    #
    # print(d)
    # MySqlOptions().conn.commit()