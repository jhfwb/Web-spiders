from clientScrapySystem.DatabaseSystem.template.keyArr import KEY_ARR
class FilterData:
    """
    过滤器。过滤数据
    """
    @staticmethod
    def filterFunction_site(data):
        """
        过滤位置：这些位置是我们需要的。
        """
        if not data:
            return None
        citys = KEY_ARR.getSiteArr()
        for city in citys:
            if data['公司名'] != None:
                if city in data['公司名']:
                    return data
            if data['地址'] != None:
                if city in data['地址']:
                    data['地址'] = data['地址'].replace(city, '|**' + city + '**|')
                    return data
            if data['城市'] != None:
                if city in data['城市']:
                    data['城市'] = data['城市'].replace(city, '|**' + city + '**|')
                    return data
            if data['信息'] != None:
                if city in data['信息']:
                    data['信息'] = data['信息'].replace(city, '|**' + city + '**|')
                    return data
            if data['产品'] != None:
                if city in data['产品']:
                    data['产品'] = data['产品'].replace(city, '|**' + city + '**|')
                    return data
        return None
    @staticmethod
    def filterFunction_products(data):
        """
        过滤产品
        """
        if not data:
            return None
        products = KEY_ARR.getKeyArr()
        for product in products:
            if data['公司名'] != None:
                if product in data['公司名']:
                    return data
            if data['产品'] != None:
                if product in data['产品']:
                    data['产品'] = data['产品'].replace(product, '|**' + product + '**|')
                    print(data)
                    return data
            if data['信息'] != None:
                if product in data['信息']:
                    data['信息'] = data['信息'].replace(product, '|**' + product + '**|')
                    return data
        return None

    @staticmethod
    def filterFunction_company_status(data):
        if not data:
            return None
        """
        过滤掉经营状况吊销的情况
        """
        if data.get('经营状况') != None:
            if "吊销" in data['经营状况'] or "注销" in data['经营状况']:
                return None
        return data
