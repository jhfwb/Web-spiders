import re

import requests
import os.path
from bs4 import BeautifulSoup
class WebPageCheck:
    def __init__(self,
        start_url_selector='',
        start_url_re_rule='',
        cacheDirPath='',
        header={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
            }):
        if cacheDirPath!='':
            cacheDirPath=cacheDirPath+'/'
        if(start_url_re_rule!=''):
            fileName_re_rule = cacheDirPath + "check-" + start_url_re_rule.replace('/', '').replace('\\', '').replace(
                '.', '').replace(':', '') + '.html'
            if os.path.isfile(fileName_re_rule):
                with open(fileName_re_rule, 'r', encoding='utf-8', newline="") as fp:
                    fileTest2 = ''.join(fp.readlines())
                    fp.close()
            else:
                resp = requests.get(start_url_re_rule, headers=header)
                fileTest2 = resp.text
                # 将其保存起来。并进行慢慢进行检测。
                with open(fileName_re_rule, 'w', encoding='utf-8', newline="") as fp:
                    fp.write(resp.text)
                    fp.close()
            soup2 = BeautifulSoup(fileTest2, "html.parser")
            self.testHtml_selector = soup2
            #提取出所有的href
            hrefs=re.findall(r'href=\"(.*?)\"',str(soup2))
            self.hrefs=hrefs
        if (start_url_selector != ''):
            fileName_selector = cacheDirPath + "check-" + start_url_selector.replace('/', '').replace('\\', '').replace(
                '.', '').replace(':', '') + '.html'
            if os.path.isfile(fileName_selector):
                with open(fileName_selector, 'r', encoding='utf-8', newline="") as fp:
                    fileTest = ''.join(fp.readlines())
                    fp.close()
            else:
                resp = requests.get(start_url_selector, headers=header)
                fileTest = resp.text
                # 将其保存起来。并进行慢慢进行检测。
                with open(fileName_selector, 'w', encoding='utf-8', newline="") as fp:
                    fp.write(resp.text)
                    fp.close()
            soup = BeautifulSoup(fileTest, "html.parser")
            self.testHtml_selector = soup
    def check_re_url(self,rules=[]):
        results={}
        losehrefs=[]
        for r in rules:
            results.setdefault(r,[])
        for href in self.hrefs:
            for rule in rules:
                try:
                    result=re.fullmatch(rule,href).string
                    results[rule].append(result)
                except:
                   losehrefs.append(href)
        results.setdefault('losehrefs',losehrefs)
        return results
    def check_selector(self,cssStr):
        try:
            return self.testHtml_selector.select(cssStr)[0]
        except:
            print("该css有误")
            return None
if __name__ == '__main__':
    #写上测试的名称


    webPageCheck=WebPageCheck(start_url_selector="https://www.11467.com/jinan/co/159221.htm",start_url_re_rule="https://b2b.11467.com/search/-540a88c55e26-pn8.htm",cacheDirPath='ache')
    a=webPageCheck.check_selector("#contact > div > dl > dd:nth-child(6)")
    b = webPageCheck.check_re_url(['.*//b2b\.11467\.com/search/-540a88c55e26-pn[\d+]+\.htm','(.+(www.11467.com)/\w+/)(co/)?\d+(\.htm)$'])
    print(b)