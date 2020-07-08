class FileUtils:
    def replaceText(self,path="",oldWord="",newWord="",encoding='utf-8'):
        fp=open(mode='r',file=path,encoding=encoding)
        lines=fp.readlines()
        for i in range(len(lines)):
            lines[i]=lines[i].replace(oldWord,newWord)
        fp.close()
        fp1=open(mode='w',file=path,encoding=encoding)
        fp1.writelines(lines)
        fp1.close()

if __name__ == '__main__':
    u=FileUtils()
    u.replaceText(path='config.xml', oldWord='9ad85f3a6da47eb6', newWord='你好')
