from _xhr_tool._utils.PathUtils import relpath
class DiskDirPath:
    # excute_datas=Path('../disk/excute_datas/').resolve()
    excute_datas=relpath('../disk/excute_datas/')
    excute_datas_err=relpath('../disk/excute_datas_err/')
    ready_send_datas=relpath('../disk/ready_send_datas/')
    sended_datas=relpath('../disk/sended_datas/')
    src_datas=relpath('../disk/src_datas/')
class DiskFilePath:
    sended_datas=relpath('../disk/sended_datas/sended_data.csv')
    ready_send_datas=relpath('../disk/ready_send_datas/ready_send_data.csv')
if __name__ == '__main__':
    print(DiskDirPath.excute_datas)