from functools import reduce
def remove_repeat_arr_inner_dict(arr,key=None):
    """
    根据key的值,对数组arr中的字典去重。
    e.g:
        [{name:'张三'},{name:'李四'},{name:'张三'}]
        >>>  from _xhr_tool._utils.arr_caculate import remove_repeat_arr_inner_dict
        >>>  arr = [{'公司名称': '张三'}, {'公司名称': '李四'}, {'公司名称': '张三'}]
        >>>  arr = remove_repeat_arr_inner_dict(arr,key='公司名称')
        >>>  输出:[{'公司名称': '张三'}, {'公司名称': '李四'}]
    :param arr:
    :param key:
    :return:
    """
    def test(x, y):
        for x1 in x:
            if x1[key] == y[key]:
                return x
        return x + [y]
    if key==None:
        arr = reduce(lambda x,y:x if y in x else x+[y], [[], ] + arr)
    else:
        arr = reduce(test, [[], ] + arr)
    return arr
if __name__ == '__main__':
    arr = [{'公司名称': '张三'}, {'公司名称': '李四'}, {'公司名称': '张三'}]
    arr=remove_repeat_arr_inner_dict(arr,key='公司名称')
    print(arr)