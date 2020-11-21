import asyncio
import logging
import math
import os
import shutil
import time

import requests
from bs4 import BeautifulSoup
from pyrogram import Client, Filters
from pyrogram.api import functions, types

from pyrobot import COMMAND_HAND_LER

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)


@Client.on_message(Filters.command("yify", COMMAND_HAND_LER) & Filters.me)
async def ytdl_(client: Client, message):
    await message.edit_text("Gettin yify recent movies. Check @uploadbot")
    uploadbot = "@uploadbot"
    BASE_URL = "https://yts.pm"
    tg_feed_link = BASE_URL + "/browse-movies"
    main_page_response = requests.get(tg_feed_link)
    main_soup = BeautifulSoup(main_page_response.text, "html.parser")
    movies_in_page = main_soup.find_all("div", class_="browse-movie-wrap")
    for movie in movies_in_page:
        movie_links = movie.div.find_all("a")
        movie_links = movie_links[1:]
        for torrent_link in movie_links:
            href_link = BASE_URL + torrent_link.get("href")
            magnetic_link_response = requests.get(
                href_link, allow_redirects=False)
            magnetic_link = magnetic_link_response.headers.get("Location")
            await client.send_message(
                chat_id=uploadbot,
                text=magnetic_link
            )
            # return False
            await asyncio.sleep(120)
