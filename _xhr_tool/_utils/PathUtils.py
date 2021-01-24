def relpath(file):
    """ 将相对路径转成绝对路径，并且该相对路径不随着入口函数变化而变化"""
    from sys import _getframe
    from pathlib import Path
    frame = _getframe(1) #获的调用该relpath()方法，的栈
    curr_file = Path(frame.f_code.co_filename) # 获得该栈对应的文件的路径
    parent_curr_file=curr_file.parent #获得上级文件夹路径
    pa=parent_curr_file.joinpath(file) #连接文件夹路径与文件
    return str(pa.resolve()) #获得绝对路径