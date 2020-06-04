import asyncio
import logging
import os
import subprocess

from pyrogram import Client, Filters
from pyrogram.api.types import ChannelParticipantAdmin
from pyrogram.errors import FloodWait

from pyrobot import COMMAND_HAND_LER

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)
                    

@Client.on_message(Filters.command(["getc"], COMMAND_HAND_LER) & Filters.me)
async def get_c(client: Client, message):
    if message.forward_from:
        return
    dir= "./temp/"
    try:
        os.makedirs("./temp/")
    except:
    	pass
    channel_username= message.text
    command = ['ls','temp','|','wc','-l' ]
    limit = message.command[1]
    channel_username = message.command[2]
    await message.edit("Downloading Media From this Channel.")
    async for msgs in client.iter_history(chat_id=channel_username[1:],limit=int(limit)):
        if msgs.document is not None:
            await client.download_media(msgs,dir)
                
    ps = subprocess.Popen(('ls', 'temp'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('wc', '-l'), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'","")
    output = output.replace("\n","")
    await message.edit("Downloaded "+limit+" files.")
             
             
             
             
             
             
@Client.on_message(Filters.command(["geta"], COMMAND_HAND_LER) & Filters.me)
async def get_c(client: Client, message):
    if message.forward_from:
        return
    dir= "./temp/"
    try:
        os.makedirs("./temp/")
    except:
    	pass
    channel_username= message.command[1][1:]
    command = ['ls','temp','|','wc','-l' ]

    await message.edit("Downloading All Media From this Channel.")
    async for msgs in client.iter_history(chat_id=channel_username):
        if msgs.document is not None:
            try:
                await client.download_media(msgs,dir) 
            except FloodWait:
                await asyncio.sleep(20)
            await client.download_media(msgs,dir)
    ps = subprocess.Popen(('ls', 'temp'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('wc', '-l'), stdin=ps.stdout)
    ps.wait()
    output = str(output)
    output = output.replace("b'","")
    output = output.replace("\n'","")
    await message.edit("Downloaded "+output+" files.")
