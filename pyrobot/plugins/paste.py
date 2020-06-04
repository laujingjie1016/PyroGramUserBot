import logging
import os

import requests
from pyrogram import Client, Filters
from requests import get, post
from requests.exceptions import HTTPError, Timeout, TooManyRedirects

from pyrobot import COMMAND_HAND_LER, TMP_DOWNLOAD_DIRECTORY

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)

DOGBIN_URL = "https://del.dog/"
NEKOBIN_URL = "https://nekobin.com/"

@Client.on_message(Filters.command(["paste"], COMMAND_HAND_LER) & Filters.me)
async def count_(client: Client, message):
    """pastes the text directly to dogbin"""
    if message.forward_from:
        return
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)
        input_str = message.command[0]
        message = "SYNTAX: `.paste <long text to include>`"
        if input_str:
            message = input_str
        elif message.reply_to_message:
            previous_message = message.reply_to_message.message_id
            if previous_message.media:
                downloaded_file_name = await client.download_media(
                    message=previous_message,
                    file_name=TMP_DOWNLOAD_DIRECTORY
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                message = ""
                for m in m_list:
                    # message += m.decode("UTF-8") + "\r\n"
                    message += m.decode("UTF-8")
                os.remove(downloaded_file_name)
            else:
                message = previous_message.message_id
                message = await client.get_messages(message.chat.id,previous_message.message_id)
        # else:
        #     message = "SYNTAX: `.paste <long text to include>`"
        py_file =  ""
        if downloaded_file_name.endswith(".py"):
            py_file += ".py"
            data = message
            key = requests.post('https://nekobin.com/api/documents', json={"content": data}).json().get('result').get('key')
            url = f'https://nekobin.com/{key}{py_file}'
            reply_text = f'Nekofied to *Nekobin* : {url}'
            await message.edit(reply_text)
        else:
            data = message
            key = requests.post('https://nekobin.com/api/documents', json={"content": data}).json().get('result').get('key')
            url = f'https://nekobin.com/{key}'
            reply_text = f'Nekofied to *Nekobin* : {url}'
            await message.edit(reply_text)
