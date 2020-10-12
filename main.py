import os
from random import choice
from graia.application import Group, Friend
from graia.application.entry import GroupMessage, FriendMessage
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Image, Plain
from graia.application import GraiaMiraiApplication
from Controller.init import bcc, app
from Model.db import DbModel
from Controller.text_writer import text_generator
from config import *

# 缓存
group_define = {}

# 图片路径
image_paths = []
image_name = os.listdir('./image')
for i in image_name:
    image_path = './image' + '/' + i
    image_paths.append(image_path)


# 个人
@bcc.receiver(FriendMessage)
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend):
    data = await app.groupList()
    for i in data:
        await app.sendFriendMessage(friend, MessageChain(__root__=[
            Plain('{} {} {}'.format(i.id, i.name, i.accountPerm))
        ]))


# 群组
@bcc.receiver(GroupMessage, priority=2)
async def group_message_handler(app: GraiaMiraiApplication, message: MessageChain, group: Group):
    # 定义功能模块
    db = DbModel(group.id)
    define_data = db.read_define_from_file()  # 读取群内定义数据

    # 写入定义
    if message.asDisplay().startswith('# 定义'):
        # msg = message.asDisplay().split(' ', 3)
        # if len(msg) == 2:
        #     await app.sendGroupMessage(group, MessageChain(__root__=[
        #         Plain('? 定义啥你倒是说啊'),
        #     ]))
        # elif len(msg) == 3:
        #     try:
        #         del define_data[msg[2]]
        #         Msg = '定义清除成功'
        #     except KeyError:
        #         Msg = '没有这个定义啊喂'
        #     await app.sendGroupMessage(group, MessageChain(__root__=[
        #         Plain(Msg)
        #     ]))
        # elif len(msg) == 4:
        #     if message.has(Image):
        #         image = Image()
        #         image.url = message.get(Image)[0].url
        #         data = [image.url]
        #     else:
        #         data = msg[3]
        #
        #     if msg[2] in define_data:
        #         Msg = '定义覆盖成功'
        #     else:
        #         Msg = '定义成功'
        #     define_data[msg[2]] = data
        #
        #     await app.sendGroupMessage(group, MessageChain(__root__=[
        #         Plain(Msg),
        #     ]))
        db.write_define_to_file(define_data)

    # 回复定义
    try:
        if message.asDisplay() in define_data:
            if type(define_data[message.asDisplay()]) == list:
                await app.sendGroupMessage(group, MessageChain(__root__=[
                    Image.fromNetworkAddress(define_data[message.asDisplay()][0])
                ]))
            else:
                await app.sendGroupMessage(group, MessageChain(__root__=[
                    Plain(define_data[message.asDisplay()])
                ]))
    except KeyError:
        pass

    # 查看定义列表
    if message.asDisplay() == '# 查看定义':
        if define_data:
            Msg = '本群所有定义：'
            for key in define_data:
                Msg = Msg + '\n' + key
        else:
            Msg = '暂无定义！'

        await app.sendGroupMessage(group, MessageChain(__root__=[
            Plain(Msg)
        ]))

    # 删除群内所有定义
    if message.asDisplay() == '# 删除定义':
        define_data = {}
        db.write_define_to_file(define_data)
        await app.sendGroupMessage(group.id, MessageChain(__root__=[
            Plain('所有定义清零成功')
        ]))


    # 回复功能模块
    if message.asDisplay() == '@妖小白':
        await app.sendGroupMessage(group, MessageChain(__root__=[
            Plain('不必找了，本帝一直都在')
        ]))
    elif message.asDisplay() == '早' or message.asDisplay() == '早安':
        await app.sendGroupMessage(group, MessageChain(__root__=[
            Plain('几点了？还早？\n')
        ]))
        await app.sendGroupMessage(group, MessageChain(__root__=[
            Plain('给爷爬！'),
        ]))
    elif '帅' in message.asDisplay() and message.asDisplay() != '真帅':
        await app.sendGroupMessage(group, MessageChain(__root__=[
            Plain("帅？帅个屁")
        ]))
    elif message.asDisplay() == '# 查看功能':
        await app.sendGroupMessage(group, MessageChain(__root__=[
            Plain(FEATURES)
        ]))
    elif message.asDisplay() == '@FlourPackage 今天的粉品是0！':
        await app.sendGroupMessage(group.id, MessageChain(__root__=[
            Plain("不会吧不会吧，不会还有粉的粉品为零吧\n这也太那个了吧")
        ]))
    elif message.asDisplay() == '呜呜呜':
        await app.sendGroupMessage(group.id, MessageChain(__root__=[
            Plain("你呜你🐎呢")
        ]))

    # 叫车功能模块
    if message.has(Image):
        if message[Image][0].imageId == '{61BB8091-C869-AE57-E0CA-6843B7CC13A9}.mirai':
            await app.sendGroupMessage(group, MessageChain(__root__=[
                Image.fromLocalFile(choice(image_paths))
            ]))

    # 文章生成模块
    if message.asDisplay().startswith('# 狗屁很通'):
        msg = message.asDisplay().split(' ', 3)
        if len(msg) == 2:
            Msg = '写作文不写题目啊喂'
        else:
            Msg = text_generator(msg[2])
        await app.sendGroupMessage(group, MessageChain(__root__=[
            Plain(Msg)
        ]))

    # if group.id == GroupID:
    #     if message.has(Image):
    #         image = Image()
    #         image.url = message.get(Image)[0].url
    #         await app.sendGroupMessage(group, MessageChain(__root__=[
    #             Plain('{}'.format(type(image.url))),
    #             Image.fromNetworkAddress(image.url)
    #         ]))
    #     else:
    #         await app.sendGroupMessage(group, MessageChain(__root__=[
    #             Plain(message.asDisplay())
    #         ]))


if __name__ == '__main__':
    app.launch_blocking()
