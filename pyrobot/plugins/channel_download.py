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
    # print(limit)
    channel_username = message.command[2]
    # print(channel_username[1:])
    # chat = await Client.get_chat("aiosetup")
    # print(chat)
    # await message.edit("Downloading Media From this Channel.")
    async for msgs in client.iter_history(chat_id=channel_username[1:],limit=int(limit)):
        # print(message.caption)
    # msgs = await Client.get_messages(channel_username, limit=int(limit))
        # with open('log.txt','w') as f:
    	    # f.write(str(msgs))
    # for msg in msgs:
        if msgs.document is not None:
            await client.download_media(msgs,dir)
    ps = subprocess.Popen(('ls', 'temp'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('wc', '-l'), stdin=ps.stdout)
    # print(output)
    ps.wait()
    output = str(output)
    output = output.replace("b'","")
    output = output.replace("\n","")
    await message.edit("Downloaded "+limit+" files.")
             
             
             
             
             
             
# @borg.on(events.NewMessage(pattern=r"\.geta", outgoing=True))  
# async def get_media(event):
#     if event.fwd_from:
#         return
#     dir= "./temp/"
#     try:
#         os.makedirs("./temp/")
#     except:
#     	pass
#     channel_username= event.text
#     command = ['ls','temp','|','wc','-l' ]
#     channel_username = channel_username[7:]
 
   
#     print(channel_username)
#     await event.edit("Downloading All Media From this Channel.")
#     msgs = await borg.get_messages(channel_username,limit=3000)
#     with open('log.txt','w') as f:
#     	f.write(str(msgs))
#     for msg in msgs:
#         if msg.media is not None:
#             try:
#                 await borg.download_media(
#                     msg,dir) 
#             except FloodWaitError as e:
#                 await asyncio.sleep(20)
# 	        # await borg.download_media(
#             #     msg,dir)          
#     ps = subprocess.Popen(('ls', 'temp'), stdout=subprocess.PIPE)
#     output = subprocess.check_output(('wc', '-l'), stdin=ps.stdout)
#     ps.wait()
#     output = str(output)
#     output = output.replace("b'","")
#     output = output.replace("\n'","")
#     await event.edit("Downloaded "+output+" files.")
