# csv代码执行器

## 1.作用简介
在csv文件的表头上输入特定代码，就能够使得该代码作用在csv文件中的数据体上。

## 2.如何使用代码？
```python
from _xhr_tool.csv_tools.csv_code_excuter import CsvExcuter
CsvExcuter().csv_execCode(inputPath='test_.csv')
# 默认生成2个文件，第一个是test__excCode.csv文件(正确执行的文件)
# 第二个是test__excCode.csv文件(错误执行，不满足正则表达式的文件)

#以下是第二种使用方式。能够自定义输入的文件
CsvExcuter().csv_execCode(inputPath='test_.csv',outputPath='right.csv',err_outputPath='err.csv')
```


## 3.csv中表头语法
> 只有当csv文件中表头的语法正确的时候才能够顺利执行

1.正常的csv文件如下：
```csv
姓名,电话
许焕燃,13805980379
施丽园,187594298789
```

2.由于我想将该csv改造成短信与电话的形式，使得短信的发送更加具备弹性。因此写下如下表头
```csv
"姓名{{ !customer= customer[0]+' 总 ' }}((re='.{2,3}'))",电话{{phone}}((re='\d{11}')),"{{message='尊敬的'+customer+',你好'}}"
许焕燃,13805980379
施丽园,187594298789
```
* 在表头项后面添加{{}}(())，{{}}中写入语法，语法遵从python语法。另外当该语法前面加上感叹号
的时候，代表该项将不被保留。
* (())中写入正则表达式，只有满足该正则表达式的时候才能够执行
否则，将被传到错误的csv中。

4.测试与使用
> 执行csv_code_excuter.py中的main方法。会有两个文件生成，保存在test_eg文件夹中。
