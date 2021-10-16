
import asyncio
from datetime import datetime

from pyrogram import Client, Filters
# from pyrogram.raw import base.storage.FilePdf
from pyrogram.api.types.storage import FilePdf
from pyrobot import COMMAND_HAND_LER
from pyrogram.api.types import Document


@Client.on_message(Filters.command("test", COMMAND_HAND_LER)  & Filters.me)
async def purge(client, message):
    if message.reply_to_message:
        print(message.reply_to_message.document)
        await client.send_document("me",document =message.reply_to_message.document.file_ref)
        # print(message.reply_to_message)
        # if isinstance(message.reply_to_message.document,Document):
        #     print(message.reply_to_message)
