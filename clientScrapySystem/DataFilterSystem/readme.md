# DataFileterSystem 文件过滤系统

## 功能
2020年12月18日11:53:05

将csv文件(爬虫数据进行划分，筛选，分类)。

目前可以区分两种1.目标客户，2.非目标客户，3.需要丢弃的数据


## 如何使用
### 几个重要文件
DataFilterSystem/template:用于设置筛选条件以及标准化模板
DataFilterSystem/srcFile：用于存放需要筛选的原始csv文件
DataFilterSystem/dealFiles：用于存放筛选过后的csv文件

### 开始程序的前置条件
1. 需要筛选的原始文件只允许是csv文件。
2. DataFilterSystem/template/customerData_template.csv中设置了筛选标准化模板
> 标准化模板：将杂乱的，未分类的数据转化成 既定的标准化的模板。其目的是为了便利后续数据的使用。
3. DataFilterSystem/template/keyArr.py为筛选位置信息的中间脚本
> 当你想要改变位置信息的时候，只需要改变其中的筛选条件即可。

### 如何开始程序？
在DataFilterSystem/srcFile中存入需要筛选的原始文件，启动在DataFilterSystem/main.py,
之后就可以在dealFiles中获得筛选后的文件啦！筛选后的文件目前分为3类。1.丢弃数据(不要的数据)
2.目标区域的有用数据 3.非目标区域的有用数据。