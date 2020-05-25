

import asyncio

import logging

import pyrogram

from pyrobot import API_HASH, APP_ID, DB_URI, HU_STRING_SESSION

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


<<<<<<< HEAD
=======
from pyrobot import HU_STRING_SESSION, APP_ID, API_HASH
>>>>>>> 8c5d80a65220510d09d9850be5dbd5406c65a205

logging.getLogger("pyrogram").setLevel(logging.WARNING)

class Main():
    @staticmethod
    def main():
        plugins = dict(
            root="pyrobot/plugins",
            # exclude=exclude_plugins
        )
        app = pyrogram.Client(
            HU_STRING_SESSION,
            api_id=APP_ID,
            api_hash=API_HASH,
            plugins=plugins
        )
        app.run()
        return app


if __name__ == "__main__":
    my_main = Main.main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(my_main)
