import logging
import os
import time
from datetime import datetime

from pyrogram import Client, Filters
from pyrogram.api import functions, types
from pyrogram.api.functions.account import UpdateProfile
from pyrogram.api.functions.photos import UpdateProfilePhoto

from pyrobot import COMMAND_HAND_LER, TMP_DOWNLOAD_DIRECTORY, LOGGER_GROUP

users = {}
afk = False
accepted_users = []
banned_users = []
afkMessage = "I'm AFK now.\n"

@Client.on_message(Filters.private)
async def check_saved(Client, msg):
    global users
    if not msg.from_user.id in users:
        users[msg.from_user.id] = 0
    await msg.continue_propagation()

@Client.on_message(Filters.user("self") & Filters.command("afk", prefixes=[".", "/", "!", "#"]))
async def afk_command(Client, msg):
    global afk
    global accepted_users
    global afkMessage
    accepted_users = []
    print(msg.command)
    if msg.command[2:]:
        afkMessage += str(msg.command[2:])
    if len(msg.command) == 1:
        await msg.edit_text("You are afk" if afk else "You are not afk")
    else:
        if msg.command[1] == "on":
            afk = True
            await  msg.edit_text("Afk enabled.")
        elif msg.command[1] == "off":
            afk = False
            await msg.edit_text("Afk disabled.")
        elif msg.command[1] == "on":
            afk = True
            await msg.edit_text("La modalità AFK è stata resettata.")
        else:
            await msg.edit_text("You are afk" if afk else "You are not afk")

@Client.on_message(Filters.private & ~Filters.user("self"))
async  def logger(Client, msg):
    print("[PM] Got a new message from: {}. Text: {}".format(
        "@" + msg.from_user.username if msg.from_user.username else msg.from_user.first_name,
        str(msg.text)[0:20]))
    await Client.send_message(
        LOGGER_GROUP,
        "[PM] Got a new message from: {}. Text: {}".format(
            "@" + msg.from_user.username if msg.from_user.username else msg.from_user.first_name,
            str(msg.text)[0:20])
    )
    await msg.continue_propagation()

@Client.on_message(Filters.private & ~Filters.user("self"))
async def on_private_afk_message(Client, msg):
    global accepted_users
    if not msg.from_user.id in accepted_users and afk:
            if users[msg.from_user.id] + 0 < int(time.time()) and not msg.from_user.id in banned_users:
                await Client.send_message(msg.chat.id,
                                 afkMessage.replace("{original_msg}", str(msg.text)),
                                 disable_web_page_preview=True)
                # users[msg.from_user.id] = int(time.time())
    # accepted_users.append(msg.from_user.id)
