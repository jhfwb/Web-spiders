from _xhr_tool.phoneRobot.connectComponent.ConnectMenager import PhoneConnectAssistant

#############################弃用，请删除
if __name__ == '__main__':
    device = PhoneConnectAssistant().usbConncet()
    PhoneProveAct.sendMessage(device,phone=13805980379,message='你好',isSend=False)
    print('哈哈')