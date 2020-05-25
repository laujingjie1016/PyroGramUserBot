import asyncio
import logging
import math
import os
import shutil
import time
import zipfile

from pyrogram import Client, Filters
from pyrogram.api import functions, types
<<<<<<< HEAD
=======
from pyrogram.api.types import DocumentAttributeVideo
>>>>>>> 8c5d80a65220510d09d9850be5dbd5406c65a205

from pyrobot import COMMAND_HAND_LER, TMP_DOWNLOAD_DIRECTORY
from pyrobot.helper_functions.display_progress_dl_up import \
    progress_for_pyrogram , progress

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)

@Client.on_message(Filters.command("zip", COMMAND_HAND_LER)  & Filters.me )
async def ytdl_(client: Client, message):
    input_str = message.command[1]
    mone = await message.edit_text("Processing ...")
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)
    if message.reply_to_message is not None:
        reply_message = message.reply_to_message
        try:
            c_time = time.time()
            downloaded_file_name = await client.download_media(
                message=message.reply_to_message,
                file_name=TMP_DOWNLOAD_DIRECTORY,
                progress=progress_for_pyrogram,
                progress_args=(
                "trying to download", message, c_time
                )
            )
            directory_name = downloaded_file_name
            await message.edit_text("Finish downloading to my local")
            zipfile.ZipFile(directory_name + '.zip', 'w', zipfile.ZIP_DEFLATED).write(directory_name)
            await client.send_document(
                chat_id=message.chat.id,
                document=directory_name + ".zip",
                caption="Zipped By @By_Azade",
                parse_mode="html",
                disable_notification=True,
                reply_to_message_id=message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    "trying to upload", message, c_time
                )
            )
            try:
                os.remove(directory_name + ".zip")
                os.remove(directory_name)
            except:
                    pass
            await message.edit_text("Task Completed")
            await asyncio.sleep(3)
            await message.delete()
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    elif input_str:
        directory_name = input_str
        zipfile.ZipFile(directory_name + '.zip', 'w', zipfile.ZIP_DEFLATED).write(directory_name)
        await message.edit_text("Local file compressed to `{}`".format(directory_name + ".zip"))
