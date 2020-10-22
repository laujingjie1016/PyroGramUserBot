"""Check your internet speed powered by speedtest.net
Syntax: .speedtest
Available Options: image, file, text"""
import logging
import time
from datetime import datetime

import speedtest
from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)



@Client.on_message(Filters.command(["speedtest"], COMMAND_HAND_LER) & Filters.me)
async def count_(client: Client, message):
    if message.forward_from:
        return
    input_str = message.command[1]
    as_text = False
    as_document = True
    if input_str == "image":
        as_document = False
    elif input_str == "file":
        as_document = True
    elif input_str == "text":
        as_text = True
    await message.edit("Calculating my internet speed. Please wait!")
    start = datetime.now()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")
    reply_msg_id = message.reply_to_message
    if reply_msg_id:
        reply_msg_id = message.reply_to_message.message_id
    try:
        response = s.results.share()
        speedtest_image = response
        if as_text:
            await message.edit("""**SpeedTest** completed in {} seconds
Download: {}
Upload: {}
Ping: {}
Internet Service Provider: {}
ISP Rating: {}""".format(ms, convert_from_bytes(download_speed), convert_from_bytes(upload_speed), ping_time, i_s_p, i_s_p_rating))
        else:
            await client.send_photo(
                chat_id=message.chat.id,
                photo=speedtest_image,
                caption="**SpeedTest** completed in {} seconds".format(ms),
                reply_to_message_id=message.message_id
            )
            await message.delete()
    except Exception as exc:
        await message.edit("""**SpeedTest** completed in {} seconds
Download: {}
Upload: {}
Ping: {}

__With the Following ERRORs__
{}""".format(ms, convert_from_bytes(download_speed), convert_from_bytes(upload_speed), ping_time, str(exc)))


def convert_from_bytes(size):
    power = 2**10
    n = 0
    units = {
        0: "",
        1: "kilobytes",
        2: "megabytes",
        3: "gigabytes",
        4: "terabytes"
    }
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"
