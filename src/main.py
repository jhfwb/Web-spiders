from _xhr_tool import Device

#发送所有短信
from _xhr_tool.mysql.connect import MySqlOptions

mySqlOptions=MySqlOptions(host='localhost', user='root', password='512124632', database='crapydatabase')
datas=mySqlOptions.find(table='messages',columns=['信息','手机','短信状态'])
device=Device()
for data in datas:
    device.act.higher.sendMessage(phone=data[1],message=[0])