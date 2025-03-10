import os
import time

from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER


@Client.on_message(Filters.command(["fwd"], COMMAND_HAND_LER) & Filters.me)
async def for_ward(client, message):
    FORWARD_TARGET = os.environ.get("FORWARD_ID")
    if not FORWARD_TARGET:
        await message.edit("You have to add Forward Target id")
        time.sleep(5)
        await message.delete()
    if message.reply_to_message:
        await message.reply_to_message.forward(chat_id=FORWARD_TARGET)
    else:
        await message.edit("You have to reply to a document for Forward")

    time.sleep(5)
    await message.delete()
