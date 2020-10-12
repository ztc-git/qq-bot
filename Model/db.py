import shelve


class DbModel(object):
    def __init__(self, group_id):
        self.group_id = repr(group_id)

    # 写入定义数据
    def write_define_to_file(self, data):
        with shelve.open('./DB/define_db') as db:
            db[self.group_id] = data

    # 读取定义数据
    def read_define_from_file(self):
        with shelve.open('./DB/define_db') as db:
            if self.group_id in db:
                define_data = db[self.group_id]
            else:
                define_data = {}
        return define_data
