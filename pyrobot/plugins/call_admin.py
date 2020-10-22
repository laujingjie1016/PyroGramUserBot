
import logging

from pyrogram import Client, Filters
from pyrogram.api.types import ChannelParticipantAdmin

from pyrobot import COMMAND_HAND_LER

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)

@Client.on_message(Filters.command(["spamadmin"], COMMAND_HAND_LER) & Filters.me)
async def spam_spot(client, message):
    if message.forward_from:
        return
    mentions = "@admin: **Spam Spotted**"
    chat = message.chat.id
    async for x in client.iter_chat_members(chat, filter="administrators"):
        mentions += f"[\u2063](tg://user?id={x.user.id})"
    reply_message = None
    if message.reply_to_message:
        reply_message = await client.get_messages(message.chat.id,message.reply_to_message.message_id)
    await message.reply(mentions)
    await message.delete()
