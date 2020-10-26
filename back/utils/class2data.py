import datetime


# 通用数据处理方法  任何继承db.Model的数据模型对象  处理成json可以解析的
# 要处理的数据格式
# 1.一个对象  type=1
# 2.对象数组  type=0
# 遍历  根据需要的属性  构造新的对象
def Class2Data(data_list, fields, type=0):
    if not type:
        list = []
        for item in data_list:
            temp = {}
            for f in fields:
                if f in [
                        'leave_time', 'return_time', 'starttime', 'endtime',
                        'pushtime', 'handletime','start_time','end_time'
                ] and getattr(item, f):
                    # 特殊数据处理 举例：时间戳——>2020-02-02 20:02:02
                    temp[f] = datetime.datetime.strftime(
                        getattr(item, f), "%Y-%m-%d %H:%M:%S")
                else:
                    temp[f] = getattr(item, f)
            list.append(temp)
    else:
        list = {}
        for f in fields:
            list[f] = getattr(data_list, f)
    return list


def Class2Data_dealDatetime(data, fields):
    list = {}
    for f in fields:
        if f == 'starttime' and getattr(data, f):
            list['startday'] = datetime.datetime.strftime(
                getattr(data, f), '%Y-%m-%d')
            list['starttime'] = datetime.datetime.strftime(
                getattr(data, f), '%H:%M')
            """
            start = datetime.datetime.strftime(getattr(data,f),'%Y-%m-%d %H:%M:%S')
            list['startday'] = start.split()[0]
            list['starttime'] = start.split()[1]
            """
        if f == 'endtime' and getattr(data, f):
            list['endday'] = datetime.datetime.strftime(
                getattr(data, f), '%Y-%m-%d')
            list['endtime'] = datetime.datetime.strftime(
                getattr(data, f), '%H:%M')
            """
            end = datetime.datetime.strftime(getattr(data, f), '%Y-%m-%d %H:%M:%S')
            list['endday'] = end.split()[0]
            list['endtime'] = end.split()[1]
            """
        if f in ['pushtime', 'handletime', 'starttime', 'endtime']:
            pass
        else:
            list[f] = getattr(data, f)
    return list