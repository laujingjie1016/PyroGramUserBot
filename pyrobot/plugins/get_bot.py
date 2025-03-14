from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER


@Client.on_message(Filters.command(["get_bot"], COMMAND_HAND_LER) & Filters.me)
async def get_bots(client, message):
    mentions = "Bots in this Channel: \n"
    input_str = message.text[9:]
    if not input_str:
        input_str = message.chat.id
    try:
        async for x in client.iter_chat_members(chat_id=input_str, filter="bots"):
            if x.status == "administrator":
                mentions += "\n ⚜️ [{}](tg://user?id={}) `{}`".format(
                    x.user.first_name, x.user.id, x.user.id)
            else:
                mentions += "\n [{}](tg://user?id={}) `{}`".format(
                    x.user.first_name, x.user.id, x.user.id)
    except Exception as e:
        mentions += " " + str(e) + "\n"
    await message.edit(mentions)
