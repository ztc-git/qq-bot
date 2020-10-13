from graia.application import GraiaMiraiApplication, Session
from graia.broadcast import Broadcast
import asyncio
from config import *


loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host=HOST,  # 填入http api服务运行的地址
        authKey=AUTHKEY,  # 填入 authKey
        account=ACCOUNT,  # 你的机器人的 qq 号
        websocket=True  # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)