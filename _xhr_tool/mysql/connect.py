#coding:utf-8
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
        查找数据
        option.find_tables(table='messages',joinConditions=[('customers',('messages.客户id','customers.id')),],columns=[])
        :param table:
        :param joinConditions:[('tableName1',(主表属性,从表属性),...),('tableName2',(主表属性,从表属性),...)]
        :param columns:
        :param conditions: [('id',1)]
        :param sort:
        :param limit:
        :return:
        """
        if len(columns)==0:
            columnsStr='*'
        else:

            columnsStr = ",".join(map(lambda x:'`'+x.split('.')[0]+'`.'+x.split('.')[1] if len(x.split('.'))==2 else '`' + x + '`', columns))
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
                    joinc+=join[0]+'='+join[1]+' AND '
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
            raise ZeroDivisionError("columns参数为空,请务必赋值")
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
        except pymysql.err.OperationalError as ee:
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
        :param table: 数据库中表的名称
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
    def update_obj(self,table='',obj={},uniqueCondition=[]):
        """
        根据虚拟对象，更新数据库中的某一条数据。更新的时候需要传入uniqueID。该数据的唯一标识字段名
        :param table: 数据库中表的名称
        :param obj: 更新的表的对象
        :param uniqueCondition: 筛选的唯一条件
        :return:
        """
        try:
            conditionsStr=" AND ".join(map(lambda x:str('`'+x[0]+'`')+'='+'\''+str(x[1])+'\'',uniqueCondition))
        except IndexError:
            raise ValueError('conditions参数异常:请确保如下方式进行__conditions=[(id,1),(name=张三)]')
        sql_where = ""
        if conditionsStr.strip() != "":
            sql_where = "WHERE " + conditionsStr

        a=self.find_tables(table=table,conditions=uniqueCondition)
        print(a)
        if len(a)!=2:
            raise KeyError('uniqueCondition:'+str(uniqueCondition)+';该键值，不是个唯一值，或者该值不存在。')
        setStr='SET '
        for item in obj.items():
            if item[1]!=None:
                setStr+=item[0]+'=\"'+str(item[1])+'\",'
        setStr=setStr[0:len(setStr)-1]

        sql = """
UPDATE """ + table + """
"""+setStr+"""
"""+sql_where+""";"""
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except pymysql.err.OperationalError as a:
            print('\033[31m-----异常sql语句------' + sql)
            self.conn.rollback()
            print("更新失败")
            raise a
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
SET """ + columeName +"""=\'"""+str(newValue)+"""\'
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
#     a=option.find_tables(table='messages',joinConditions=[('customers',('客户id','id')),],columns=[])
    obj={'id': None, '公司': '南通新帝克单丝科技股份有限公司', '关键词': None, '主营产品': None, '使用规格': None, '地址': '南通市港闸区闸西工贸园区', '省': None,
     '城市': None, '县': None, '乡': None, '电话1': '15962976515', '电话2': '13914392016', '电话3': '13646271917', '经营状况': '存续',
     '公司简介': '合成纤维、针纺织品及原辅材料生产、销售；化纤技术开发；服装及原辅材料、电器设备、普通机械及配件加工、销售；印染助剂、工艺美术品、珠宝、纺丝用防腐剂及油剂销售；自营和代理上述商品的进出口业务（国家限定公司经营或禁止进出口的商品除外）。（经环保验收合格后方可生产）（依法须经批准的项目，经相关部门批准后方可开展经营活动）许可项目：道路货物运输（不含危险货物）（依法须经批准的项目，经相关部门批准后方可开展经营活动，具体经营项目以审批结果为准）',
     '公司产品介绍': None, '备注': None, '_url': None, '爬虫网': None, 'reliability': None, '数据状态': '需天眼查查验',
     '电话集': ['0513-83571568', '0513-85560702', '15962976515', '13914392016', '13646271917', '18862730614',
             '18206298375', '18651073908', '15850506568', '18921482168', '18248620132', '15951319535', '15190822712',
             '13814726275', '15950812018', '13962707382', '13813719515'], '客户': '马海燕', '注册资本': '2272.5万人民币',
     '实缴资本': '2272.5万人民币', '行业': '批发业'}
    print(obj)
    a=option.update_obj(table='company',uniqueID='公司',obj=obj)
    # a=option.update(table='messages',columeName='客户id',newValue=6,conditions=[('id',1)])
    #
    # print(d)
    # MySqlOptions().conn.commit()