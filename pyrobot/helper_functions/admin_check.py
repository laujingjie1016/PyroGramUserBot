#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyrogram import Message


async def admin_check(message: Message) -> bool:
    client = message._client
    chat_id = message.chat.id
    user_id = message.from_user.id

    check_status = await client.get_chat_member(
        chat_id=chat_id,
        user_id=user_id
    )
    admin_strings = [
        "creator",
        "administrator"
    ]
    # https://git.colinshark.de/PyroBot/PyroBot/src/branch/master/pyrobot/modules/admin.py#L69
    if check_status.status not in admin_strings:
        return False
    else:
        return True
