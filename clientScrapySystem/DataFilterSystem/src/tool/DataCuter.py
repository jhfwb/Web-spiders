from clientScrapySystem.DataFilterSystem.src.tool.FilterData import FilterData


class DataCuter:# 数据分割器，过滤后分为
    #寻找关键字。
    def dataCuterByKey(self,datas):
        """
        关键词过滤器
        """
        datas1=[]
        datas2=[]
        for data in datas:
            dataF=FilterData.filterFunction_key_words(data)
            if dataF!=None:
                datas1.append(dataF)
            else:
                datas2.append(data)
        return (datas1,datas2)
    def dataCuterBySite(self,datas):
        """
        位置过滤器
        """
        datas1 = []
        datas2 = []
        for data in datas:
            dataF = FilterData.filterFunction_site(data)
            if dataF!= None:
                datas1.append(dataF)
            else:
                datas2.append(data)
        return (datas1, datas2)
        return datas
