from _utils.RUtils import tool

import requests
import re
import os
import zipfile

from _xhr_tool._utils import relpath


class ChromeDriverDownloader:
    """
    谷歌核心的下载器。
    1.下载的网址。
    2.解压
    """
    # 大版本号
    # 子版本号
    saveDirPath = '' # 保存的文件夹路径
    down_url='' #下载的网址
    chromeDriver_version='' #需要下载的谷歌谷歌版本号
    def __init__(self,chromeDriver_version=''):
        self.chromeDriver_version=chromeDriver_version
    def download(self,download_url,saveDirPath=''):#下载谷歌压缩包，并保存在指定文件夹
        """
        下载文件，并保存在指定文件夹中
        :param download_url: 被下载文件的url
        :param saveDirPath: 被保存的文件夹路径，可以是绝对路径或者相对路径
        :return:
        """
        print('以下是下载链接:')
        print(download_url)
        file = requests.get(download_url)
        if saveDirPath!='':
            saveDirPath=relpath(saveDirPath)
            if not os.path.exists(saveDirPath):
                raise FileNotFoundError('该文件夹找不到:'+saveDirPath)
            saveDirPath=saveDirPath+'\\'
        with open(saveDirPath+os.path.basename(download_url), 'wb') as zip_file:  # 保存文件到脚本所在目录
            zip_file.write(file.content)
        return saveDirPath+os.path.basename(download_url)
    def un_zip(self,zipFilePath,saveDirPath,isDelZip=False):
        """
        解压文件到指定目录
        :param zipFilePath: 压缩包的路径
        :param saveDirPath: 保存的文件名
        :param isDelZip: 解压完毕后是否删除该压缩文件
        :return:
        """
        if not os.path.exists(zipFilePath):
            raise FileNotFoundError('该压缩包找不到:' + zipFilePath)
        if not os.path.exists(saveDirPath):
            raise FileNotFoundError('该文件夹找不到:' + saveDirPath)
        f = zipfile.ZipFile(zipFilePath, 'r')
        for file in f.namelist():
            f.extract(file, relpath(saveDirPath))
        f.close()
        if isDelZip:
        #删除掉解压包
            os.remove(zipFilePath)

class MyChromeDriverDownloader(ChromeDriverDownloader):
    url = 'http://npm.taobao.org/mirrors/chromedriver/'
    def getVersionsDict(self,url):
        """
        查询最新的Chromedriver版本。返回chromedriver的版本号字典。
        :param url: 镜像地址
        :return: str
        """
        rep = requests.get(url).text
        time_list = []                                          # 用来存放版本时间
        time_version_dict = {}                                  # 用来存放版本与时间对应关系
        result = re.compile(r'\d.*?/</a>.*?Z').findall(rep)     # 匹配文件夹（版本号）和时间
        for i in result:
            time = i[-24:-1]                                    # 提取时间
            version = re.compile(r'.*?/').findall(i)[0]         # 提取版本号
            time_version_dict[time] = version                   # 构建时间和版本号的对应关系，形成字典
            time_list.append(time)                              # 形成时间列表
        return time_version_dict
    def downloadChromeDriverByVersion(self,versionID='',saveDirPath='',index=-1):
        selectVersionId_1=[]
        selectVersionId_2=[]
        selectVersionId_3=[]
        selectVersionId_4=[]
        selectVersionId_5=[]
        versionIDs=versionID.split('.')
        driverVersions=self.getVersionsDict(self.url)
        if len(driverVersions)==0:
            raise ValueError('无法从'+self.url+'爬取到当前谷歌版本号！请确认该网站可以正确登录！')
        for key,value in driverVersions.items():
            if len(versionIDs)>=1 and value.startswith(versionIDs[0]) :
                selectVersionId_1.append(value)
            if len(versionIDs)>=2 and value.startswith(versionIDs[0]+'.'+versionIDs[1]):
                selectVersionId_2.append(value)
            if len(versionIDs)>=3 and value.startswith(versionIDs[0] + '.' + versionIDs[1]+'.'+versionIDs[2]):
                selectVersionId_3.append(value)
            if len(versionIDs)>=4 and value.startswith(versionIDs[0] + '.' + versionIDs[1] + '.' + versionIDs[2]+'.'+versionIDs[3]):
                selectVersionId_4.append(value)
            if len(versionIDs)>=5 and value.startswith(versionIDs[0] + '.' + versionIDs[1] + '.' + versionIDs[2]+'.'+versionIDs[3]+'.'+versionIDs[4]):
                selectVersionId_5.append(value)
        selectVersion=""
        if len(selectVersionId_1)!=0:
            selectVersion=selectVersionId_1[index]
        if len(selectVersionId_2)!=0:
            selectVersion=selectVersionId_2[index]
        if len(selectVersionId_3) != 0:
            selectVersion = selectVersionId_3[index]
        if len(selectVersionId_4) != 0:
            selectVersion = selectVersionId_4[index]
        if len(selectVersionId_5) != 0:
            selectVersion = selectVersionId_5[index]
        zipFile=self.download(download_url=self.url+selectVersion+'chromedriver_win32.zip',saveDirPath=saveDirPath)
        self.un_zip(zipFilePath=zipFile,saveDirPath=saveDirPath,isDelZip=True)
        tool().print('成功下载:['+zipFile+"]文件;并将其解压到:["+relpath(saveDirPath)+']文件夹中')
if __name__ == "__main__":
    url = 'http://npm.taobao.org/mirrors/chromedriver/'
    downloader=MyChromeDriverDownloader()
    a=downloader.downloadChromeDriverByVersion(versionID='89.0.4389.82',saveDirPath='../test')
    c='89.0.4389.82'
