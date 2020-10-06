import os
from random import choice
from graia.application import Group, Friend
from graia.application.entry import GroupMessage, FriendMessage
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Image, Plain
from graia.application import GraiaMiraiApplication
from init import bcc, app
from db import *
from text_writer import text_generator


group_define = {}
a = ['想我了就来找我，别弄得满手都是', '你摸摸我衣服，看我是不是做你男人的料', '你是无边的宇宙，我这颗小星球，就在你心中转动',
     '今晚来我家，我爸妈不在', '请你认真向风学学，怎么往我怀里钻']

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
    define_data = read_define_from_file(group_id=group.id) # 读取群内定义数据
    if message.asDisplay().startswith('# 定义'):
        msg = message.asDisplay().split(' ', 3)
        if len(msg) == 1 or len(msg) == 2:
            await app.sendGroupMessage(group, MessageChain(__root__=[
                Plain('? 定义啥你倒是说啊'),
            ]))
        elif len(msg) == 3:
            try:
                del define_data[msg[2]]
                Msg = '定义清除成功'
            except KeyError:
                Msg = '没有这个定义啊喂'
            await app.sendGroupMessage(group, MessageChain(__root__=[
                Plain(Msg)
            ]))
        elif len(msg) == 4:
            if message.has(Image):
                image = Image()
                image.url = message.get(Image)[0].url
                data = [image.url]
            else:
                data = msg[3]

            if msg[2] in define_data:
                Msg = '定义覆盖成功'
            else:
                Msg = '定义成功'
            define_data[msg[2]] = data

            await app.sendGroupMessage(group, MessageChain(__root__=[
                Plain(Msg),
            ]))
        write_define_to_file(define_data, group.id)

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
    elif message.asDisplay().startswith('帅'):
        await app.sendGroupMessage(group, MessageChain(__root__=[
            Plain("帅？帅个屁")
        ]))

    # 叫车功能模块
    if message.has(Image):
        if message[Image][0].imageId == '{61BB8091-C869-AE57-E0CA-6843B7CC13A9}.mirai':
            await app.sendGroupMessage(group, MessageChain(__root__=[
                Image.fromLocalFile(choice(image_paths))
            ]))

    if (group.id == 870256396) and message.asDisplay() == '妖小白':
        await app.sendGroupMessage(group, MessageChain(__root__=[
            Plain('{}'.format(choice(a)))
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

    # if group.id == 870256396 :
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
