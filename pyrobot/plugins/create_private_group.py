import logging
import time

from pyrogram import Client, Filters
from pyrogram.api.functions.messages import GetUnreadMentions
from pyrogram.api.types import Channel, Chat, Dialog, User

from pyrobot import COMMAND_HAND_LER

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)



@Client.on_message(Filters.regex(pattern=".create(.*b|g|c)") & Filters.me)
async def count_(client: Client, message):
    print(message.matches[0])
    if '.createb' in message.matches[0]:
        print("tru")
    
    # if message.matches.match == "createb"
    # group_typ
    # if group_type == "g":
    #     await client.create_supergroup()