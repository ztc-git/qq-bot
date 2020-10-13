import os
from random import choice
from graia.application import Group, Friend
from graia.application.entry import GroupMessage, FriendMessage
from graia.application.message.elements.internal import Plain
from graia.application import GraiaMiraiApplication
from Controller.init import bcc, app
from Controller.define_controller import *
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
    define_func = DefineFunc(group.id)
    # 写入定义
    if message.asDisplay().startswith('# 定义'):
        Msg = define_func.write_define(message)
        await app.sendGroupMessage(group.id, MessageChain(__root__=[
            Plain(Msg)
        ]))


    # # 回复定义
    data = define_func.reply_definition_message(message)
    if data:
        if data[0]:
            await app.sendGroupMessage(group.id, MessageChain(__root__=[
                Image.fromNetworkAddress(data[1])
            ]))
        else:
            await app.sendGroupMessage(group.id, MessageChain(__root__=[
                Plain(data[1])
            ]))

    # 查看定义列表
    if message.asDisplay() == '# 查看定义':
        Msg = define_func.look_through_definition_list()
        await app.sendGroupMessage(group, MessageChain(__root__=[
            Plain(Msg)
        ]))

    # 删除群内所有定义
    if message.asDisplay() == '# 删除定义':
        Msg = define_func.delete_all_definition()
        await app.sendGroupMessage(group.id, MessageChain(__root__=[
            Plain(Msg)
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

    if group.id == GroupID:
        if message.has(Image):
            image = Image()
            image.url = message.get(Image)[0].url
            await app.sendGroupMessage(group, MessageChain(__root__=[
                Plain('{}'.format(message)),
                Image.fromNetworkAddress(image.url),
                Plain('{}'.format(message.get(Plain)[0].text))
            ]))
        else:
            await app.sendGroupMessage(group, MessageChain(__root__=[
                Plain(message.asDisplay())
            ]))


if __name__ == '__main__':
    app.launch_blocking()
