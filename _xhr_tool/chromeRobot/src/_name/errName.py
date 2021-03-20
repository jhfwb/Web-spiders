class responseErr:
    elementNotFind='elementNotFind'
    """元素未找到"""
    elementClickFalse='elementClickFalse'
    """元素点击失败，该元素也许存在，但是被折叠起来了，无法被点击"""
    urlAskErr='urlAskErr'
    """url访问失败:url错误，或者没网"""
    inputwordsErr = 'inputwordsErr'
    """键入失败，可能由于输入框无法输入。或者选择器不是输入框"""
    timeOutErr='timeOutErr'
    """超过时间错误，一般是访问超时，或者是获取资源，获取页面url超时"""
    elementAndNameErr='elementAndNameErr'
    """click_byName 这个方法可能会遇到，元素和名称对应错误"""





