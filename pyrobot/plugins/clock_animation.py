# (c) @UniBorg
# Original written by @UniBorg edit by @INF1N17Y

import asyncio
import logging
from collections import deque

from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)


@Client.on_message(Filters.command(["clockanim"], COMMAND_HAND_LER) & Filters.me)
async def clock(client: Client, message):
    if message.forward_from:
        return
    deq = deque(list("🕙🕘🕗🕖🕕🕔🕓🕒🕑🕐🕛"))
    for _ in range(48):
        await asyncio.sleep(0.1)
        await message.edit("".join(deq))
        deq.rotate(1)
