#_*_encoding:utf-8_*_
import configparser
import sys
import uuid
from xml.dom.minicompat import NodeList

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from xml.dom.minidom import parse

from src.GYS_pySpiders.utils.CommonUtils import CommonUtils
class IniConfigUtils:
    """

    """
    def __init__(self):
        # cf = configparser.ConfigParser()
        # cf.read("setting.ini", encoding="utf-8")
        # self.功能 = cf.get("4life", "功能")
        pass
import os

class XmlConfigUtils:
    def __init__(self):
        self.path= 'config.xml'
        self.document = parse(self.path)#
        self.configDocument = self.document.documentElement
        self.configDocumentObj=self.loadObjectByTag("root")

    #局部更新。
    def initXML(self):
        """
        初始化xml文档。为xml文档中添加_id。如果没有的话
        """
        arr=self.getAllElements()
        for element in arr:
            if element.getAttribute("_id")=="":
                element.setAttribute("_id",str(uuid.uuid1()))
        # def updata()
    def updata(self,obj=""):
        """
        核心方法。
        更新文档。将obj保存到虚拟document中。并保存到本地。
        如果obj没有传入，则会启用self.obj
        """
        if obj=="":
            obj=self.configDocumentObj
        #将obj更新到document中
        self.updataDocumentByObj(obj)
        fp = open(self.path, 'w',encoding='utf-8')
        self.document.writexml(fp, addindent='\t', newl='\n', encoding="utf-8")

        pass
    def getAllElements(self):
        arr=[]
        def getElments(arr,elemnt):
            arr1 = elemnt.childNodes
            for next in arr1:
                if "Element"  in str(next):
                    arr.append(next)
                    getElments(arr,next)
                elif "NodeList" in str(type(next)):
                    for n  in next:
                        getElments(arr,n)
        arr.append(self.configDocument)
        getElments(arr,self.configDocument)
        return arr

    def getElmentById(self,_id):
        arr=self.getAllElements()
        for element in arr:
            if _id==element.getAttribute("_id"):
                return element
        return None


    def updataDocumentByObj(self,obj):
        """
        将obj虚拟对象更新到xml的虚拟对象--document中。
        局部更新，推荐使用

        :param obj Object 必须是一个对象，不能是数组。必须有属性_id。否则会报错
        """
        try:
            _id=obj["_id"]
        except:
            raise ValueError("传入的obj对象在虚拟dom中查询不到，对应的_id。请求确保该id存在，且没有错误")
        element=self.getElmentById(_id)
        newElement =self.createXMLElementByObj(obj)
        doc= element.parentNode
        doc.removeChild(element)
        doc.appendChild(newElement)

        return True

    #根据内存对象，更新整个xml文件。谨慎使用！！！！！！
    def updataAllXmlByObj(self,obj):
        root=self.createXMLElementByObj(obj)
        fp = open(self.path, 'w')
        root.writexml(fp, addindent='\t', newl='\n', encoding="utf-8")
        self.document=parse((self.path))
        self.configDocument=self.document.documentElement
    def createXMLElementByObj(self,obj):
        """
        根据对象。创建一个element元素。obj对象，必须满足指定要求才能创建:如：必须有_name属性。
        创建完后，自动会自动创建一个特殊属性为_id。创建后
        下面是obj的模板
        """
        def creatElemet(obj):
            tagName = obj['_name']
            element = self.document.createElement(tagName)
            #创建_id属性
            if element.getAttribute("_id")=="":
                element.setAttribute("_id",str(uuid.uuid1()))
            for item in obj.items():
                if item[0]=="_name":
                    pass
                elif item[0]=="_children":
                    arr=obj['_children']
                    for chi in arr:
                        element.appendChild(creatElemet(chi))
                else:
                    element.setAttribute(item[0],item[1])
            return element
        if type(obj)==type([]):
            arr=NodeList()
            for o in obj:
                arr.append(creatElemet(o))
            return arr
        else:
            return creatElemet(obj)


    def get(self,tagName,*attrs):
        """
        根据标签，和标签的属性。获得一个Element对象。有且只返回一个

        :param tagName 标签名称
                *attrs 多元组。每个元组有两个值。(key,value)
        e.g. x1.get('website',("webName","顺企网" ),("allowed_domains","11467.com"))
        :return DOM Element对象  依赖于xml.dom.minidom
        """
        tags=self.configDocument.getElementsByTagName(tagName)
        for tag in tags:
            sign=1
            for attr in attrs:
                if tag.getAttribute(attr[0])!=attr[1]:
                    sign=0
                    break
                else:
                    pass
            if sign==1:
                return tag
        return None
    def loadObjectByTag(self,tag):
        """
        根据标签，装载为对象。

        :param: tag:标签名称。 string类型/DOM Element类型

        整个便签转化为{}.并且转化后的对象必定包含属性_name（赋值标签名）
        --标签内的属性则转化为对象的属性
        --标签底下的子标签则转化为_children属性。这个属性必定对应一个数组。其中保存着子标签转化的对象
        --如果传来的tag所对应的标签有多个。则会转化为一个数组。
        --参数如果是字符串类型。会将所有等同于字符串的标签名装再进去。因此：为了避免这种情况。
            建议其参数（tag）传入一个DOM Element对象。这样就避免了因为名字重复导致转载了您不需要的元素。
        --传参错误。会抛出ValueErrow
        e.g
        <website  webName="顺企网" name="_pySpider">
            <rules id="1">
            <rules/>
        </website>
        ====>
        {
             '_name':'website',
            'webName':'顺企网',
            'name':'_pySpider',
            '_children',[{
                '_name':'rules',
                'id':'1'
            }]
        }
        rely:xml.dom.minidom
        """
        def loadSingleObj(tag):
            obj={}
            obj.setdefault('_name',tag.tagName)
            #获得这个标签所有的属性
            attrs=tag.attributes
            # print(childrenTag)
            for item in attrs.items():
                obj.setdefault(item[0], item[1])
            #获得这个标签所有的子类对象
            childrenTags=tag.childNodes
            for childrenTag in childrenTags:
                if "Text" in str(type(childrenTag)):#文本节点
                    pass
                elif "Element" in str(type(childrenTag)):#
                    if "_children" in obj.keys():
                        obj.get("_children").append(loadSingleObj(childrenTag))
                    else:
                        obj.setdefault("_children",[loadSingleObj(childrenTag)])
            return obj
        ####检查参数、参数处理与转化
        tags=""
        if type(tag)==type(""):
            tags=self.document.getElementsByTagName(tag)
        elif  "Element" in str(type(tag)):
            tags=tag
        elif  "NodeList" in str(type(tag)):
            for t in tag:
                if "Element" not in str(type(t)):
                    raise ValueError("传入的值不是str类型，也不是Element类型",t)
            tags=tag
        else:
            raise ValueError("传入的值不是str类型，也不是Element类型",tag)
        ####
        arr=[]
        if "NodeList" in str(type(tags)):
            for tag in tags:
                arr.append(loadSingleObj(tag))
            if len(arr)==1:
                return arr[0]
            return arr
        else:
            return loadSingleObj(tags)





if __name__ == '__main__':

    x1=XmlConfigUtils()
    print(x1.configDocumentObj)
    x1.updata()

    # root=x1.loadObjectByTag("root")
    # root[0]['_children'][0].setdefault("ii","111")
    # print(root[0]['_children'][0])
    # x1.updataXmlByObj(root[0]['_children'][0])
    # x1.updataXmlByObj()
    # x1.initXML()
    # x1.initXML()
    # x1.updata()
    # # x=x1.configDocument
    # # datas=x.getElementsByTagName("website")[0].getElementsByTagName("data")
    # # a= x1.loadObjectByTag(datas)
    # # print(a)
    # # x1.get('website',("webName","顺企网1" ))
    # # obj=x1.get('website',("webName","顺企网" ),("allowed_domains","11467.com"))
    # #
    # website=x1.loadObjectByTag("website")
    # print(website)
    # # a=x1.updataXML(website)
    # obj=x1.createXMLElementByObj(website)
    # obj2 = x1.loadObjectByTag(obj)
    # print(obj2)
    #
    # # print(a)
    # # print(obj,"修改前")
    # # a=x1.updataXML(obj1)
    # # print(a,"修改后")
    # # print(type(x1.configDocument.getElementsByTagName("website")))
