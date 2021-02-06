# csv数据过滤器
## 主要功能
### 1.实现csv数据去重：
```python

datas=[{'1':'哈哈'},{'1':'哈哈'},{'1':'嘻嘻'},{'1':'嘻嘻2'},{'1':'哈哈'}]
datas=CsvDataRemoveRepeat()._removeRepeatByKey(key='1',datas=datas)
print(datas) ##输出[{'1': '哈哈'}, {'1': '嘻嘻2'}, {'1': '嘻嘻'}]
```