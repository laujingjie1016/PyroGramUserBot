import asyncio
import logging
import os
from datetime import datetime

import barcode
# from barcode.writer import ImageWriter
from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER, TMP_DOWNLOAD_DIRECTORY

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)
                    
@Client.on_message(Filters.command("barcode", COMMAND_HAND_LER)  & Filters.me)
async def barcode_(client: Client, message):
    print(message)
    await message.edit("Creating barcode")
    start = datetime.now()
    input_str = message.command[1]
    message = "SYNTAX: `.barcode <long text to include>`"
    # reply_msg_id = message.reply_to_message.message_id
    if input_str:
        message = input_str
    elif message.reply_to_message:
        # reply_msg_id = message.reply_to_message.message_id
        if message.reply_to_message.media:
            downloaded_file_name = await client.download_media(
                message=message.reply_to_message,
                file_name=TMP_DOWNLOAD_DIRECTORY
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = ""
            for m in m_list:
                message += m.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = message.reply_to_message.text
    else:
        message = "SYNTAX: `.barcode <long text to include>`"
    bar_code_type = "code128"
    try:
        bar_code_mode_f = barcode.get(bar_code_type, message, writer=ImageWriter())
        filename = bar_code_mode_f.save(bar_code_type)
        await client.send_document(
            chat_id=message.chat.id,
            document=filename,
            reply_to_message_id=message.message_id,
        )
        os.remove(filename)
    except Exception as e:
        return
    end = datetime.now()
    ms = (end - start).seconds
    await message.edit("Created BarCode in {} seconds".format(ms))
    await asyncio.sleep(5)
    await message.delete()
