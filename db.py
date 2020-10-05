import shelve


# 写入定义数据
def write_define_to_file(data, group_id):
    with shelve.open('./DB/define_db') as db:
        db[repr(group_id)] = data


# 读取定义数据
def read_define_from_file(group_id):
    with shelve.open('./DB/define_db') as db:
        if repr(group_id) in db:
            define_data = db[repr(group_id)]
        else:
            define_data = {}
    return define_data
