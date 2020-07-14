class KEY_ARR:
    @staticmethod
    def getSiteArr(self):
        citys = ["广东", "深圳", "珠海", "汕头", "佛山", "韶关市", "湛江", "肇庆", "江门", "茂名", "惠州", "梅州", "汕尾", "河源", "阳江", "清远", "东莞",
                 "中山", "潮州", "揭阳", "云浮",
                 "福建", "福州", "厦门", "宁德", "莆田", "泉州", "漳州", "龙岩", "三明", "南平"
                  "江西", "南昌", "景德", "萍乡", "九江", "新余", "鹰潭", "赣州",
                 "吉安", "宜春", "抚州", "上饶",
                 "湖南",
                 ]
        return citys

    def getKeyArr(self,mode="all"):
        """
        mode:all | main | minor
        """
        products_1=["高强涤纶","吊装带", "牵引带", "拖车带","紧固带", "输送带", "土工", "特斯林", "渔网", "缆绳",
                  "工业涤纶缝纫线", "高强涤纶缝纫线", "胶管", "灯箱广告布", "篷布",
                  "涂层织物", "帆布", "安全带","消防水带","宠物带","安全气囊","工业布","农用水带"]
        products_2=["织带","网","编制","涤纶","涂层布","盘管", "泳池面料","高强缝纫线","电缆","鞋面"]
        if mode=="main":
            return products_1
        elif mode=='minor':
            return products_2
        elif mode=="all":
            return products_1+products_2
        return None

