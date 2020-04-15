
import asyncio
import logging
import os

import pyrogram
from pyrogram import Client, Filters
from pyrogram.api import functions, types
from pyrogram.errors import *

from pyrobot import TMP_DOWNLOAD_DIRECTORY

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)
admin = 'administrator'
creator = 'creator'
ranks = [admin, creator]

async def ReplyCheck(message):
    if not message.reply_to_message:
        await message.edit(f"`{message.command[0]}` needs to be a reply.")
        await asyncio.sleep(2)
        await message.delete()
    elif message.reply_to_message.from_user.is_self:
        await message.edit(f"I can't {message.command[0]} myself.")
        await asyncio.sleep(2)
        await message.delete()
    else:
        return True

async def AdminCheck(message):
    SELF = await pyrogram.Client.get_chat_member(
        chat_id=message.chat.id,
        user_id=message.from_user.id)

    if SELF.status not in ranks:
        await message.edit("__I'm not Admin!__")
        await asyncio.sleep(2)
        await message.delete()

    else:
        if SELF.status is not admin:
            return True
        elif SELF.permissions.can_restrict_members:
            return True
        else:
            await message.edit("__No permissions to restrict Members__")

async def RestrictFailed(message):
    await message.edit(f"I can't {message.command[0]} this user.")


@Client.on_message(Filters.command(r"setgic", ".")  & Filters.me)
async def set_gic(client: Client, message):
    peer = await client.resolve_peer(message.chat.id)
    if not message.text.isalpha() and message.text not in ("/", "!"):
        if message.reply_to_message.message_id:
            reply_message = message.reply_to_message.message_id
    await message.edit("Downloading Profile Picture to my local ...")
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):  
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)   
    photo = None
    try:
        photo = await client.download_media(
            message=message.reply_to_message,
            file_name=TMP_DOWNLOAD_DIRECTORY
        )
    except Exception as e: 
        await message.edit(str(e))
    else:
        if photo:
            await message.edit("now, Uploading to group pic ...")
            try:
                photo = types.InputChatUploadedPhoto(file=await client.save_file(photo))
                await client.send(
                    functions.messages.EditChatPhoto(
                        chat_id=peer.chat_id,
                        photo=photo
                    )
                )
            except Exception as e:  
                await message.edit(str(e))
            else:
                await message.edit("Group profile picture was succesfully changed")
    try:
        os.remove(photo)
    except Exception as e:  
        logger.warnning(str(e)) 



@Client.on_message(Filters.command(r"ban", ".")  & Filters.me)
async def bann(client: Client, message):
    
    SELF = await client.get_chat_member(chat_id=message.chat.id,user_id=message.from_user.id)
    if SELF.status in ranks:
        if await ReplyCheck(message) is True:
            name = message.reply_to_message.from_user.first_name
            user_id = message.reply_to_message.from_user.id
            try:
                await client.kick_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.reply_to_message.from_user.id,
                    until_date=0
                )
                await message.edit("[{}](tg://user?id={}) banned!".format(name,user_id))
                await client.delete_messages(
                    chat_id=message.chat.id,
                    message_ids=message.reply_to_message.message_id
                )
            except UserAdminInvalid:
                pass


@Client.on_message(Filters.command(r"unban", ".")  & Filters.me)
async def unbann(client: Client, message):
    print(message)
    SELF = await client.get_chat_member(chat_id=message.chat.id,user_id=message.from_user.id)
    if SELF.status in ranks:
        if await ReplyCheck(message) is True:
            name = message.reply_to_message.from_user.first_name
            user_id = message.reply_to_message.from_user.id
            try:
                await client.unban_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.reply_to_message.from_user.id
                )
                await message.edit("[{}](tg://user?id={}) unbanned!".format(name,user_id))
            except UserAdminInvalid:
                pass
        # else:



@Client.on_message(Filters.command(r"promote", ".")  & Filters.me)
async def promot(client: Client, message):
    SELF = await client.get_chat_member(chat_id=message.chat.id,user_id=message.from_user.id)
    if await ReplyCheck(message) is True:
        if SELF.status in ranks:
            try:
                x = await client.promote_chat_member(
                    message.chat.id, message.reply_to_message.from_user.id,
                    can_change_info=False,
                    can_delete_messages=1,
                    can_invite_users=1,
                    can_pin_messages=1,
                    can_promote_members=False,
                    can_restrict_members=1
                )
                if x:
                    await message.edit("`Successfully promoted.`")
            except PermissionError:
                await RestrictFailed(message)

@Client.on_message(Filters.command(r"demote", ".")  & Filters.me)
async def demot(client: Client, message):
    SELF = await client.get_chat_member(chat_id=message.chat.id,user_id=message.from_user.id)
    if await ReplyCheck(message) is True:
        if SELF.status in ranks:
            try:
                x = await client.promote_chat_member(
                    message.chat.id, message.reply_to_message.from_user.id,
                    can_change_info=False,
                    can_delete_messages=False,
                    can_invite_users=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                    can_restrict_members=False
                )
                if x:
                    await message.edit("`Successfully demoted.`")
            except PermissionError:
                await RestrictFailed(message)

@Client.on_message(Filters.me & Filters.command(['botlist'], ['.']))
async def bot_list(client: Client, message):
    try:
        x =await client.get_chat_members(message.chat.id, filter="bots")
        bots = "\n"
        for a in range(len(x)):
            if x[a].user.is_bot:
                name = x[a].user.first_name
                bot_id = x[a].user.id
                bots += "🤖 [{}](tg://user?id={})\n".format(name,bot_id)
        await message.edit("Botlist in {}\n{}".format(message.chat.title,bots))
    except MessageTooLong:
        await message.edit(
            "This group is filled with bots as hell. Uploading bots list as file."
        )
        with open('botlist.txt', 'w') as file:
            file.write(bots)
            file.close()
        await client.send_document(
            chat_id=message.chat.id,
            document="botlist.txt",
            caption='Bots in {}'.format(message.chat.title),
            reply_to_message_id=message.message_id,
        )
        os.remove("botlist.txt")


@Client.on_message(Filters.me & Filters.command(['ghostlist'], ['.']))
async def ghost_list(client: Client, message):
    try:
        x =await client.get_chat_members(message.chat.id)
        deleted = "\n"
        for a in range(len(x)):
            if x[a].user.is_deleted:
                name = x[a].user.status
                deleted_id = x[a].user.id
                deleted += "👻 [{}](tg://user?id={})\n".format(name,deleted_id)
        await message.edit("Deleted Accounts in {}:\n{}".format(message.chat.title,deleted))
    except MessageTooLong:
        await message.edit(
            "This group is filled with deleted account as hell. Uploading bots list as file."
        )
        with open('deleted_account.txt', 'w') as file:
            file.write(deleted)
            file.close()
        await client.send_document(
            chat_id=message.chat.id,
            document="deleted_account.txt",
            caption='Deleted Account in {}'.format(message.chat.title),
            reply_to_message_id=message.message_id,
        )
        os.remove("deleted_account.txt")
        




            
# @borg.on(events.NewMessage(outgoing=True, pattern="^.unban(?: |$)(.*)")) # pylint:disable=E0602
# async def unban(eventUnban):
#     if not eventUnban.text[0].isalpha() and eventUnban.text[0] \
#             not in ("/", "#", "@", "!"):
#         chat = await eventUnban.get_chat()
#         admin = chat.admin_rights
#         creator = chat.creator
#         if not admin and not creator:
#             await eventUnban.edit("`I am not an admin!`")
#             return
#         await eventUnban.edit("Unbanning!`")
#         user = await get_user_from_event(eventUnban)
#         if user:
#             pass
#         else:
#             return
#         try:
#             await eventUnban.client(EditBannedRequest(
#                 eventUnban.chat_id,
#                 user.id,
#                 UNBAN_RIGHTS
#             ))
#             await eventUnban.edit("```Unbanned Successfully```")
#             if ENABLE_LOG:
#                 await eventUnban.client.send_message(
#                     LOGGING_CHATID,
#                     "#UNBAN\n"
#                     f"USER: [{user.first_name}](tg://user?id={user.id})\n"
#                     f"CHAT: {eventUnban.chat.title}(`{eventUnban.chat_id}`)"
#                 )
#         except UserIdInvalidError:
#             await eventUnban.edit("`Uh oh my unban logic broke!`")

 
# @borg.on(events.NewMessage(outgoing=True, pattern="^.mute(?: |$)(.*)")) # pylint:disable=E0602
# async def mute(eventMute):
#     if not eventMute.text[0].isalpha() and eventMute.text[0] not in ("/", "#", "@", "!"):
#         try:
#             from sql_helpers.spam_mute_sql import mute
#         except AttributeError:
#             await eventMute.edit("`Running on Non-SQL mode!`")
#             return
#         chat = await eventMute.get_chat()
#         admin = chat.admin_rights
#         creator = chat.creator
#         if not admin and not creator:
#             await eventMute.edit("`I am not an admin!`")
#             return

#         user = await get_user_from_event(eventMute)
#         if user:
#             pass
#         else:
#             return
#         self_user = await eventMute.client.get_me()
#         if user.id == self_user.id:
#             await eventMute.edit("`Hands too short, can't duct tape myself...\n(ヘ･_･)ヘ┳━┳`")
#             return
#         await eventMute.edit("`Gets a tape!`")
#         if mute(eventMute.chat_id, user.id) is False:
#             return await eventMute.edit('`Error! User probably already muted.`')
#         else:
#             try:
#                 await eventMute.client(
#                     EditBannedRequest(
#                         eventMute.chat_id,
#                         user.id,
#                         MUTE_RIGHTS
#                     )
#                 )
#                 await eventMute.edit("`Safely taped!`")
#                 if ENABLE_LOG:
#                     await eventMute.client.send_message(
#                         LOGGING_CHATID,
#                         "#MUTE\n"
#                         f"USER: [{user.first_name}](tg://user?id={user.id})\n"
#                         f"CHAT: {eventMute.chat.title}(`{eventMute.chat_id}`)"
#                     )
#             except UserIdInvalidError:
#                 return await eventMute.edit("`Uh oh my mute logic broke!`")


# @borg.on(events.NewMessage(outgoing=True, pattern="^.unmute(?: |$)(.*)")) # pylint:disable=E0602
# async def unmute(eventUnMute):
#     if not eventUnMute.text[0].isalpha() and eventUnMute.text[0] \
#             not in ("/", "#", "@", "!"):
#         chat = await eventUnMute.get_chat()
#         admin = chat.admin_rights
#         creator = chat.creator
#         if not admin and not creator:
#             await eventUnMute.edit("`I am not an admin!`")
#             return
#         try:
#             from sql_helpers.spam_mute_sql import unmute
#         except AttributeError:
#             await eventUnMute.edit("`Running on Non-SQL mode!`")
#             return
#         await eventUnMute.edit('```Unmuting...```')
#         user = await get_user_from_event(eventUnMute)
#         if user:
#             pass
#         else:
#             return
#         if unmute(eventUnMute.chat_id, user.id) is False:
#             return await eventUnMute.edit("`Error! User probably already unmuted.`")
#         else:

#             try:
#                 await eventUnMute.client(
#                     EditBannedRequest(
#                         eventUnMute.chat_id,
#                         user.id,
#                         UNBAN_RIGHTS
#                     )
#                 )
#                 await eventUnMute.edit("```Unmuted Successfully```")
#             except UserIdInvalidError:
#                 await eventUnMute.edit("`Uh oh my unmute logic broke!`")
#                 return

#             if ENABLE_LOG:
#                 await eventUnMute.client.send_message(
#                     LOGGING_CHATID,
#                     "#UNMUTE\n"
#                     f"USER: [{user.first_name}](tg://user?id={user.id})\n"
#                     f"CHAT: {eventUnMute.chat.title}(`{eventUnMute.chat_id}`)"
#                 )


# @borg.on(events.NewMessage(incoming=True)) # pylint:disable=E0602
# async def muter(mutedMessage): 
#     try:
#         from sql_helpers.spam_mute_sql import is_muted
#         from sql_helpers.gmute_sql import is_gmuted
#     except AttributeError:
#         return
#     muted = is_muted(mutedMessage.chat_id)
#     gmuted = is_gmuted(mutedMessage.sender_id)
#     rights = ChatBannedRights(
#         until_date=None,
#         send_messages=True,
#         send_media=True,
#         send_stickers=True,
#         send_gifs=True,
#         send_games=True,
#         send_inline=True,
#         embed_links=True,
#     )
#     if muted:
#         for i in muted:
#             if str(i.sender) == str(mutedMessage.sender_id):
#                 await mutedMessage.delete()
#                 await mutedMessage.client(EditBannedRequest(
#                     mutedMessage.chat_id,
#                     mutedMessage.sender_id,
#                     rights
#                 ))
#     for i in gmuted:
#         if i.sender == str(mutedMessage.sender_id):
#             await mutedMessage.delete()


# @borg.on(events.NewMessage(outgoing=True, pattern="^.gmute(?: |$)(.*)")) # pylint:disable=E0602
# async def gmute(eventGmute):
#     if not eventGmute.text[0].isalpha() and eventGmute.text[0] not in ("/", "#", "@", "!"):
#         chat = await eventGmute.get_chat()
#         admin = chat.admin_rights
#         creator = chat.creator
#         if not admin and not creator:
#             await eventGmute.edit("`I am not an admin!`")
#             return
#         try:
#             from sql_helpers.gmute_sql import gmute
#         except AttributeError:
#             await eventGmute.edit("`Running on Non-SQL mode!`")
#             return

#         user = await get_user_from_event(eventGmute)
#         if user:
#             pass
#         else:
#             return
#         await eventGmute.edit("`Grabs a huge, sticky duct tape!`")
#         if gmute(user.id) is False:
#             await eventGmute.edit('`Error! User probably already gmuted.\nRe-rolls the tape.`')
#         else:
#             await eventGmute.edit("`Haha Yash! Globally taped!`")

#             if ENABLE_LOG:
#                 await eventGmute.client.send_message(
#                     LOGGING_CHATID,
#                     "#GMUTE\n"
#                     f"USER: [{user.first_name}](tg://user?id={user.id})\n"
#                     f"CHAT: {eventGmute.chat.title}(`{eventGmute.chat_id}`)"
#                 )


# @borg.on(events.NewMessage(outgoing=True, pattern="^.ungmute(?: |$)(.*)")) # pylint:disable=E0602
# async def ungmute_(eventUnGmute):
#     if not eventUnGmute.text[0].isalpha() and eventUnGmute.text[0] \
#             not in ("/", "#", "@", "!"):
#         chat = await eventUnGmute.get_chat()
#         admin = chat.admin_rights
#         creator = chat.creator
#         if not admin and not creator:
#             await eventUnGmute.edit("`I am not an admin!`")
#             return
#         try:
#             from sql_helpers.gmute_sql import ungmute
#         except AttributeError:
#             await eventUnGmute.edit("`Running on Non-SQL mode!`")
#             return
#         user = await get_user_from_event(eventUnGmute)
#         if user:
#             pass
#         else:
#             return
#         await eventUnGmute.edit('```Ungmuting...```')

#         if ungmute(user.id) is False:
#             await eventUnGmute.edit("`Error! User probably not gmuted.`")
#         else:
#             await eventUnGmute.edit("```Ungmuted Successfully```")

#             if ENABLE_LOG:
#                 await eventUnGmute.client.send_message(
#                     LOGGING_CHATID,
#                     "#UNGMUTE\n"
#                     f"USER: [{user.first_name}](tg://user?id={user.id})\n"
#                     f"CHAT: {eventUnGmute.chat.title}(`{eventUnGmute.chat_id}`)"
#                 )


# @borg.on(events.NewMessage(outgoing=True, pattern="^.delusers(?: |$)(.*)")) # pylint:disable=E0602
# async def rm_deletedacc(eventDeletedAccs):
#     if not eventDeletedAccs.text[0].isalpha() and eventDeletedAccs.text[0] not in ("/", "#", "@", "!"):
#         con = eventDeletedAccs.pattern_match.group(1)
#         del_u = 0
#         del_status = "`No deleted accounts found, Group is cleaned as Hell`"

#         if not eventDeletedAccs.is_group:
#             await eventDeletedAccs.edit("`This command is only for groups!`")
#             return
#         if con != "clean":
#             await eventDeletedAccs.edit("`Searching for ded af accounts...`")
#             async for user in eventDeletedAccs.client.iter_participants(
#                     eventDeletedAccs.chat_id
#             ):
#                 if user.deleted:
#                     del_u += 1

#             if del_u > 0:
#                 del_status = f"found **{del_u}** deleted account(s) in this group \
#                 \nClean them by using .delusers clean"
#             await eventDeletedAccs.edit(del_status)
#             return
#         chat = await eventDeletedAccs.get_chat()
#         admin = chat.admin_rights
#         creator = chat.creator
#         if not admin and not creator:
#             await eventDeletedAccs.edit("`I am not an admin here!`")
#             return
#         await eventDeletedAccs.edit("`Deleting deleted accounts...\nOh I can do that?!?!`")
#         del_u = 0
#         del_a = 0
#         async for user in eventDeletedAccs.client.iter_participants(
#                 eventDeletedAccs.chat_id
#         ):
#             if user.deleted:
#                 try:
#                     await eventDeletedAccs.client(
#                         EditBannedRequest(
#                             eventDeletedAccs.chat_id,
#                             user.id,
#                             BANNED_RIGHTS
#                         )
#                     )
#                 except ChatAdminRequiredError:
#                     await eventDeletedAccs.edit("`I don't have ban rights in this group`")
#                     return
#                 except UserAdminInvalidError:
#                     del_u -= 1
#                     del_a += 1
#                 await eventDeletedAccs.client(
#                     EditBannedRequest(
#                         eventDeletedAccs.chat_id,
#                         user.id,
#                         UNBAN_RIGHTS
#                     )
#                 )
#                 del_u += 1
#         if del_u > 0:
#             del_status = f"Cleaned **{del_u}** deleted account(s)"
#         if del_a > 0:
#             del_status = f"Cleaned **{del_u}** deleted account(s) \
#             \n**{del_a}** deleted admin accounts are not removed."
#         await eventDeletedAccs.edit(del_status)


# @borg.on(events.NewMessage(outgoing=True, pattern="^.adminlist$")) # pylint:disable=E0602
# async def listadmins(eventListAdmins):
#     if not eventListAdmins.text[0].isalpha() and eventListAdmins.text[0] not in ("/", "#", "@", "!"):
#         if not eventListAdmins.is_group:
#             await eventListAdmins.edit("I don't think this is a group.")
#             return
#         info = await eventListAdmins.client.get_entity(eventListAdmins.chat_id)
#         title = info.title if info.title else "this chat"
#         mentions = f'<b>Admins in {title}:</b> \n'
#         try:
#             async for user in eventListAdmins.client.iter_participants(
#                     eventListAdmins.chat_id, filter=ChannelParticipantsAdmins
#             ):
#                 if not user.deleted:
#                     link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
#                     userid = f"<code>{user.id}</code>"
#                     mentions += f"\n{link} {userid}"
#                 else:
#                     mentions += f"\nDeleted Account <code>{user.id}</code>"
#         except ChatAdminRequiredError as err:
#             mentions += " " + str(err) + "\n"
#         await eventListAdmins.edit(mentions, parse_mode="html")


# @borg.on(events.NewMessage(outgoing=True, pattern="^.pin(?: |$)(.*)")) # pylint:disable=E0602
# async def pinmessage(eventPinMessage):
#     if not eventPinMessage.text[0].isalpha() and eventPinMessage.text[0] not in ("/", "#", "@", "!"):
#         chat = await eventPinMessage.get_chat()
#         admin = chat.admin_rights
#         creator = chat.creator
#         if not admin and not creator:
#             await eventPinMessage.edit("`I am not an admin!`")
#             return
#         to_pin = eventPinMessage.reply_to_msg_id
#         if not to_pin:
#             await eventPinMessage.edit("`Reply to a message to pin it.`")
#             return
#         options = eventPinMessage.pattern_match.group(1)
#         is_silent = True
#         if options.lower() == "loud":
#             is_silent = False
#         try:
#             await eventPinMessage.client(UpdatePinnedMessageRequest(eventPinMessage.to_id, to_pin, is_silent))
#         except BadRequestError:
#             await eventPinMessage.edit("`I don't have sufficient permissions!`")
#             return
#         await eventPinMessage.edit("`Pinned Successfully!`")
#         user = await get_user_from_id(eventPinMessage.from_id, eventPinMessage)
#         if ENABLE_LOG:
#             await eventPinMessage.client.send_message(
#                 LOGGING_CHATID,
#                 "#PIN\n"
#                 f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
#                 f"CHAT: {eventPinMessage.chat.title}(`{eventPinMessage.chat_id}`)\n"
#                 f"LOUD: {not is_silent}"
#             )


# @borg.on(events.NewMessage(outgoing=True, pattern="^.kick(?: |$)(.*)")) # pylint:disable=E0602
# async def kick(eventKickUser):
#     if not eventKickUser.text[0].isalpha() and eventKickUser.text[0] not in ("/", "#", "@", "!"):
#         chat = await eventKickUser.get_chat()
#         admin = chat.admin_rights
#         creator = chat.creator
#         if not admin and not creator:
#             await eventKickUser.edit("`I am not an admin!`")
#             return
#         user = await get_user_from_event(eventKickUser)
#         if not user:
#             await eventKickUser.edit("`Couldn't fetch user.`")
#             return
#         await eventKickUser.edit("`Kicking this users...`")
#         try:
#             await eventKickUser.client(
#                 EditBannedRequest(
#                     eventKickUser.chat_id,
#                     user.id,
#                     KICK_RIGHTS
#                 )
#             )
#             await sleep(.5)
#         except BadRequestError:
#             await eventKickUser.edit("`I don't have sufficient permissions!`")
#             return
#         await eventKickUser.client(
#             EditBannedRequest(
#                 eventKickUser.chat_id,
#                 user.id,
#                 ChatBannedRights(until_date=None)
#             )
#         )
#         await eventKickUser.edit(f"[{user.first_name}](tg://user?id={user.id})` `atıldı` !`")
#         if ENABLE_LOG:
#             await eventKickUser.client.send_message(
#                 LOGGING_CHATID,
#                 "#KICK\n"
#                 f"USER: [{user.first_name}](tg://user?id={user.id})\n"
#                 f"CHAT: {eventKickUser.chat.title}(`{eventKickUser.chat_id}`)\n"
#             )


# @borg.on(events.NewMessage(outgoing=True, pattern="^.userslist ?(.*)")) # pylint:disable=E0602
# async def list_users(eventListUsers):
#     if not eventListUsers.text[0].isalpha() and eventListUsers.text[0] not in ("/", "#", "@", "!"):
#         if not eventListUsers.is_group:
#             await eventListUsers.edit("Are you sure this is a group?")
#             return
#         info = await eventListUsers.client.get_entity(eventListUsers.chat_id)
#         title = info.title if info.title else "this chat"
#         mentions = 'Users in {}: \n'.format(title)
#         try:
#             if not eventListUsers.pattern_match.group(1):
#                 async for user in eventListUsers.client.iter_participants(eventListUsers.chat_id):
#                     if not user.deleted:
#                         mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
#                     else:
#                         mentions += f"\nDeleted Account `{user.id}`"
#             else:
#                 searchq = eventListUsers.pattern_match.group(1)
#                 async for user in eventListUsers.client.iter_participants(eventListUsers.chat_id, search=f'{searchq}'):
#                     if not user.deleted:
#                         mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
#                     else:
#                         mentions += f"\nDeleted Account `{user.id}`"
#         except ChatAdminRequiredError as err:
#             mentions += " " + str(err) + "\n"
#         try:
#             await eventListUsers.edit(mentions)
#         except MessageTooLongError:
#             await eventListUsers.edit("Damn, this is a huge group. Uploading users lists as file.")
#             file = open("userslist.txt", "w+")
#             file.write(mentions)
#             file.close()
#             await eventListUsers.client.send_file(
#                 eventListUsers.chat_id,
#                 "userslist.txt",
#                 caption='Users in {}'.format(title),
#                 reply_to=eventListUsers.id,
#             )
#             remove("userslist.txt")

# @borg.on(admin_cmd(pattern="undlt ?(.*)")) # pylint:disable=E0602
# async def _(event):
#     if event.fwd_from:
#         return
#     c = await event.get_chat()
#     if c.admin_rights or c.creator:
#         a = await borg.get_admin_log(event.chat_id,limit=5, edit=False, delete=True)
#         # print(a[0].old.message)
#         deleted_msg = "Deleted message in this group:"
#         for i in a:
#             deleted_msg += "\n👉`{}`".format(i.old.message)
#         await event.edit(deleted_msg)
#     else:
#         await event.edit("`You need administrative permissions in order to do this command`")
#         await asyncio.sleep(3)
#         await event.delete()


# async def get_user_from_event(event):
#     if event.reply_to_msg_id:
#         previous_message = await event.get_reply_message()
#         user_obj = await event.client.get_entity(previous_message.from_id)
#     else:
#         user = event.pattern_match.group(1)
#         if user.isnumeric():
#             user = int(user)
#         if not user:
#             await event.edit("`Pass the user's username, id or reply!`")
#             return
#         if event.message.entities is not None:
#             probable_user_mention_entity = event.message.entities[0]

#             if isinstance(probable_user_mention_entity, MessageEntityMentionName):
#                 user_id = probable_user_mention_entity.user_id
#                 user_obj = await event.client.get_entity(user_id)
#                 return user_obj
#         try:
#             user_obj = await event.client.get_entity(user)
#         except (TypeError, ValueError) as err:
#             await event.edit(str(err))
#             return None
#     return user_obj

# async def get_user_from_id(user, event):
#     if isinstance(user, str):
#         user = int(user)
#     try:
#         user_obj = await event.client.get_entity(user)
#     except (TypeError, ValueError) as err:
#         await event.edit(str(err))
#         return None
#     return user_obj
