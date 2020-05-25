# Thanks to @AvinashReddy3108 for this plugin

"""
Audio and video downloader using Youtube-dl
.yta To Download in mp3 format
.ytv To Download in mp4 format
"""
import asyncio
import logging
import math
import os
import shutil
import time

from pyrogram import Client, Filters
from pyrogram.api import functions, types
from pyrogram.api.types import DocumentAttributeVideo
from pyrogram.errors import BadRequest, MessageIdInvalid
from youtube_dl import YoutubeDL
from youtube_dl.utils import (ContentTooShortError, DownloadError,
                              ExtractorError, GeoRestrictedError,
                              MaxDownloadsReached, PostProcessingError,
                              UnavailableVideoError, XAttrMetadataError)

from pyrobot import COMMAND_HAND_LER, TMP_DOWNLOAD_DIRECTORY
from pyrobot.helper_functions.display_progress_dl_up import \
    progress_for_pyrogram

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)


DELETE_TIMEOUT = 5

async def progress(current, total, message, start, type_of_ps, file_name=None):
    """Generic progress_callback for uploads and downloads."""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            ''.join("█" for i in range(math.floor(percentage / 10))),
            ''.join("░" for i in range(10 - math.floor(percentage / 10))),
            round(percentage, 2))
        tmp = progress_str + \
            "{0} of {1}\nETA: {2}".format(
                humanbytes(current),
                humanbytes(total),
                time_formatter(estimated_total_time)
            )
        if file_name:
            await message.edit("{}\nFile Name: `{}`\n{}".format(
                type_of_ps, file_name, tmp))
        else:
            await message.edit("{}\n{}".format(type_of_ps, tmp))


def humanbytes(size):
    """Input size in bytes,
    outputs in a human readable format"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " day(s), ") if days else "") + \
        ((str(hours) + " hour(s), ") if hours else "") + \
        ((str(minutes) + " minute(s), ") if minutes else "") + \
        ((str(seconds) + " second(s), ") if seconds else "") + \
        ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    return tmp[:-2]

@Client.on_message(Filters.command("yta", COMMAND_HAND_LER)  & Filters.me )
async def ytdl_(client: Client, message):
    
    """ For .ytdl command, download media from YouTube and many other sites. """
    url = message.command[1]
    type = message.command[1]
    out_folder = TMP_DOWNLOAD_DIRECTORY + "youtubedl/"
    thumb_image_path = TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"
    if not os.path.isdir(out_folder):
        os.makedirs(out_folder)
    await message.edit_text("`Preparing to download...`")

    if type :
        opts = {
            'format':'bestaudio',
            'addmetadata':True,
            'key':'FFmpegMetadata',
            'writethumbnail':True,
            'embedthumbnail':True,
            'prefer_ffmpeg':True,
            'geo_bypass':True,
            'nocheckcertificate':True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl':out_folder+'%(id)s.mp3',
            'quiet':True,
            'logtostderr':False
        }
        video = False
        song = True
    try:
        await message.edit_text("`Fetching data, please wait..`")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
        filename = sorted(get_lst_of_files(out_folder, []))
    except DownloadError as DE:
        await message.edit_text(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await message.edit_text("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await message.edit_text(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await message.edit_text("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await message.edit_text("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await message.edit_text("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await message.edit_text(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await message.edit_text("`There was an error during info extraction.`")
        return
    except Exception as e:
        await message.edit_text(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        thumb = f"{out_folder + ytdl_data['id']}.mp3"[:(len(f"{out_folder + ytdl_data['id']}.mp3")-4)] + ".jpg"
        file_path = f"{out_folder + ytdl_data['id']}.mp3"
        song_size = file_size(file_path)
        await message.edit_text(f"`Preparing to upload song:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*")
        await client.send_audio(
            chat_id=message.chat_id,
            audio=f"{out_folder + ytdl_data['id']}.mp3",
            caption=ytdl_data['title'] + "\n" + f"`{song_size}`",
            supports_streaming=True,
            progress=progress_for_pyrogram,
                progress_args=(
                    "trying to upload", message, c_time
                )
        )
        os.remove(f"{out_folder + ytdl_data['id']}.mp3")
        await asyncio.sleep(2)
        await message.delete()
        shutil.rmtree(out_folder)
    
    
        
@Client.on_message(Filters.command("ytv", COMMAND_HAND_LER)  & Filters.me )
async def ytdl_vid(client: Client, message):
    """ For .ytdl command, download media from YouTube and many other sites. """
    url = message.command[1]
    type = message.command[1]
    out_folder = TMP_DOWNLOAD_DIRECTORY + "youtubedl/"
    thumb_image_path = TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"
    if not os.path.isdir(out_folder):
        os.makedirs(out_folder)
    await message.edit_text("`Preparing to download...`")
    if type :
        opts = {
            'format':'best',
            'addmetadata':True,
            'key':'FFmpegMetadata',
            'prefer_ffmpeg':True,
            'getthumbnail':True,
            'embedthumbnail': True,
            'writethumbnail': True,
            'geo_bypass':True,
            'nocheckcertificate':True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'outtmpl':out_folder+'%(id)s.mp4',
            'logtostderr':False,
            'quiet':True
        }
        song = False
        video = True

    try:
        await message.edit_text("`Fetching data, please wait..`")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
        filename = sorted(get_lst_of_files(out_folder, []))
    except DownloadError as DE:
        await message.edit_text(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await message.edit_text("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await message.edit_text(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await message.edit_text("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await message.edit_text("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await message.edit_text("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await message.edit_text(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await message.edit_text("`There was an error during info extraction.`")
        return
    except Exception as e:
        await message.edit_text(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if video:
        for single_file in filename:
            file_path = f"{out_folder + ytdl_data['id']}.mp4"
            video_size = file_size(file_path)
            image = f"{ytdl_data['id']}.jpg"
            thumb = f"{out_folder + ytdl_data['id']}.jpg"
            x = await message.edit_text(f"`Preparing to upload video:`\
            \n**{ytdl_data['title']}**\
            \nby *{ytdl_data['uploader']}*")
            await client.send_document(
                chat_id=message.chat.id,
                document=f"{out_folder + ytdl_data['id']}.mp4",
                caption=ytdl_data['title'] + "\n" + f"`{video_size}`",
                thumb=thumb
            )
            os.remove(f"{out_folder + ytdl_data['id']}.mp4")
            await asyncio.sleep(2)
            await x.delete()
        shutil.rmtree(out_folder)



def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)
