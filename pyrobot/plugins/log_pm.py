# import asyncio
# import logging
# import os
# import sys
# from datetime import datetime

# from pyrogram import Client, Filters

# from pyrobot import COMMAND_HAND_LER, LOG_PM_ACTIVE, PM_LOGGR_BOT_API_ID


# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.WARN)

# global NO_PM_LOG_USERS
# NO_PM_LOG_USERS = []


# @Client.on_message(Filters.text & Filters.private)
# async def log(client, message):
#     if LOG_PM_ACTIVE and  message.chat.type != "bot":
#         chat = await client.resolve_peer(message.chat.id)
#         if chat.user_id not in NO_PM_LOG_USERS:
#             try:
#                 e = await client.resolve_peer(PM_LOGGR_BOT_API_ID)
#                 fwd_message = await client.forward_messages(
#                     chat_id=e.chat_id,
#                     from_chat_id=chat.user_id,
#                     message_ids=message.message_id
#                 )
#             except Exception as e:
#                 # logger.warning(str(e))
#                 exc_type, exc_obj, exc_tb = sys.exc_info()
#                 fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#                 print(exc_type, fname, exc_tb.tb_lineno)
#                 print(e)
