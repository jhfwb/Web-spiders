from clientScrapySystem.DatabaseSystem.src.DatesTransfer import DatesTransfer
from clientScrapySystem.DatabaseSystem.utils.DatabaseHandler import DatabaseHandler
# 功能一 将smelter中的数据变成统一数据
# 功能二 将smelter中的数据进行分类与划分
# 功能三 从任意数据库中取出数据
# 功能四 从任意数据库中保存数据

# bol=CsvToXlsx().working2()
# 将semlter所有数据转移过去。如果在中央数据库已经存在的数据，则不会被转移过去。
DatesTransfer(databaseHandler=DatabaseHandler(),fromDatabse='smelter',
              toDatabases=['0_初始客户群','其他产品客户群','其他区域客户群'],num=2).\
            transferFilter(DatesTransfer.fun_template)