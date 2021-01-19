import re

if __name__ == '__main__':
    # {{customer = customer[0] + '总'}}(re='.{2,3}')
    请输入正则表达式=r'.{2,3}'
    请输入需要判断的字符串='吴总裁11'
    a = re.fullmatch(请输入正则表达式,请输入需要判断的字符串)
    if a==None:
        print("该字符串不符合正则表达式，无法通过")
    else:
        print("该字符串符合正则表达式，通过!!")