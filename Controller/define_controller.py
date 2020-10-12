from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Image

class DefineFunc(object):
    def __init__(self, define_data):
        self.define_data = define_data

    # 写入定义
    def write_define(self, message: MessageChain):
        msg = message.split(' ', 3)
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
        return Msg

    # 回复定义
    def reply_definition_message(self, message: MessageChain):



