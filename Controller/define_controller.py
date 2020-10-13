from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Image
from Model.db import DbModel


class DefineFunc(object):
    def __init__(self, group_id):
        self.db = DbModel(group_id)
        self.define_data = self.db.read_define_from_file()

    # 写入定义
    def write_define(self, message: MessageChain):
        msg = message.asDisplay().split(' ', 3)
        if len(msg) == 2:
            Msg = '？ 定义啥你倒是说啊'
        elif len(msg) == 3:
            try:
                del self.define_data[msg[2]]
                Msg = '定义清除成功'
            except KeyError:
                Msg = '没有这个定义啊喂'
        elif len(msg) == 4:
            if message.has(Image):
                image = Image()
                image.url = message.get(Image)[0].url
                data = [image.url]
            else:
                data = msg[3]

            if msg[2] in self.define_data:
                Msg = '定义覆盖成功'
            else:
                Msg = '定义成功'
            self.define_data[msg[2]] = data

        self.db.write_define_to_file(self.define_data)
        return Msg

    # 回复定义
    def reply_definition_message(self, message: MessageChain):
        if message.asDisplay() in self.define_data:
            if type(self.define_data[message.asDisplay()]) == list:
                Msg = self.define_data[message.asDisplay()][0]
                is_image = True
            else:
                Msg = self.define_data[message.asDisplay()]
                is_image = False
            return [is_image, Msg]

    # 查看定义
    def look_through_definition_list(self):
        if self.define_data:
            Msg = '本群所有定义：'
            for key in self.define_data:
                Msg = Msg + '\n' + key
        else:
            Msg = '暂无定义！'
        return Msg

    # 删除所有定义
    def delete_all_definition(self):
        if self.define_data:
            self.define_data = {}
            self.db.write_define_to_file(self.define_data)
            Msg = '所有定义清零成功'
        else:
            Msg = '没定义还删个屁哟'
        return Msg


