"""Count the Number of Dialogs you have in your Telegram Account
Syntax: .count"""
import logging
import time

from pyrogram import Client, Filters
from pyrogram.api.functions.messages import GetUnreadMentions
from pyrogram.api.types import Channel, Chat, Dialog, User

from pyrobot import COMMAND_HAND_LER

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)


@Client.on_message(Filters.command(["count"], COMMAND_HAND_LER) & Filters.me)
async def count_(client: Client, message):
    """Command to get stats about the account"""
    waiting_message = await message.edit('`Collecting stats, please wait..`')

    channel = []
    channel_unread_msg = []
    channel_unread_mention = []
    channel_creator = []
    channel_admin = []
    group = []
    group_unread_msg = []
    group_unread_mention = []
    group_creator = []
    group_admin = []
    super_group = []
    super_group_unread_msg = []
    super_group_unread_mention = []
    super_group_creator = []
    super_group_admin = []
    bot = []
    bot_unread_msg = []
    bot_unread_mention = []
    user = []
    user_unread_msg = []
    user_unread_mention = []
    private = []
    private_unread_msg = []
    private_unread_mention = []

    async for dialog in client.iter_dialogs():
        entity = dialog.chat.type
        if entity == "channel":
            channel.append(dialog)
            channel_unread_mention.append(dialog.unread_mentions_count)
            channel_unread_msg.append(dialog.unread_messages_count)
            channel_creator.append(dialog.chat.is_creator)
            channel_admin.append(dialog.chat.permissions)
        elif entity == "group":
            group.append(dialog)
            group_unread_mention.append(dialog.unread_mentions_count)
            group_unread_msg.append(dialog.unread_messages_count)
            group_creator.append(dialog.chat.is_creator)
            group_admin.append(dialog.chat.permissions)
        elif entity == "supergroup":
            super_group.append(dialog)
            super_group_unread_mention.append(dialog.unread_mentions_count)
            super_group_unread_msg.append(dialog.unread_messages_count)
            super_group_creator.append(dialog.chat.is_creator)
            super_group_admin.append(dialog.chat.permissions)
        elif entity == "bot":
            bot.append(dialog)
            bot_unread_mention.append(dialog.unread_mentions_count)
            bot_unread_msg.append(dialog.unread_messages_count)
        elif entity == "user":
            user.append(dialog)
            user_unread_mention.append(dialog.unread_mentions_count)
            user_unread_msg.append(dialog.unread_messages_count)
        elif entity == "private":
            private.append(dialog)
            private_unread_mention.append(dialog.unread_mentions_count)
            private_unread_msg.append(dialog.unread_messages_count)
    my = await client.get_me()
    my_name = my.first_name
    response = f'🔸 **Stats for {my_name}** \n\n'
    response += f'**Private Chats:** {len(private) + len(bot)} \n'
    response += f'   • `Users: {len(private)}` \n'
    response += f'   • `Bots: {len(bot)}` \n'
    response += f'**Groups:** {len(group)} \n'
    response += f'**Channels:** {len(channel)} \n'
    response += f'**Admin in Groups:**\n'
    response += f'   • `Creator: {len(group_creator) + len(super_group_creator)}` \n'
    response += f'   • `Admin Rights: {len(group_admin) + len(super_group_admin)}` \n'
    response += f'**Admin in Channels:**\n'
    response += f'   • `Creator: {len(channel_creator)}` \n'
    response += f'   • `Admin Rights: {len(channel_admin)}` \n'
    # response += f'**Unread Message:** {len(bot_unread_msg) + len(channel_unread_msg) + len(group_unread_msg) + len(private_unread_msg) + len(super_group_unread_msg) + len(user_unread_msg)} \n'
    # response += f'**Unread Mentions:** {len(bot_unread_mention) + len(channel_unread_mention) + len(group_unread_mention) + len(private_unread_mention) + len(super_group_unread_mention) + len(user_unread_mention)} \n\n'
    await message.edit(response)
    del channel
    del channel_unread_msg
    del channel_unread_mention
    del channel_creator
    del channel_admin
    del group
    del group_unread_msg
    del group_unread_mention
    del group_creator
    del group_admin
    del super_group
    del super_group_unread_msg
    del super_group_unread_mention
    del super_group_creator
    del super_group_admin
    del bot
    del bot_unread_msg
    del bot_unread_mention
    del user
    del user_unread_msg
    del user_unread_mention
    del private
    del private_unread_msg
    del private_unread_mention
