import logging

import wikipedia
from pyrogram import Client, Filters
from pyrogram.api import functions, types

from pyrobot import COMMAND_HAND_LER

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)


@Client.on_message(Filters.command("wikipedia", COMMAND_HAND_LER)  & Filters.me )
async def ytdl_(client: Client, message):
    
    x =await message.edit_text("Processing ...")
    input_str = message.command[1:]
    print(input_str)
    result = ""
    wikipedia.set_lang("tr")
    results = wikipedia.search(input_str)
    for s in results:
        page = wikipedia.page(s)
        url = page.url
        result += f"> [{s}]({url}) \n"
    await client.send_message(
        chat_id=message.chat.id,
        text="WikiPedia **Search**: {} \n\n **Result**: \n\n{}".format(input_str, result),
        disable_web_page_preview=True
    )
    await x.delete()
    # await message.edit_text("WikiPedia **Search**: {} \n\n **Result**: \n\n{}".format(input_str, result))
