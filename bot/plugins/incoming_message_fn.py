#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K / Akshay C / @AbirHasan2005

# the logging things

import datetime
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

from bot.database import Database
import os, time, asyncio, json
from bot.localisation import Localisation
from bot import (
    DOWNLOAD_LOCATION,
    AUTH_USERS,
    LOG_CHANNEL,
    UPDATES_CHANNEL,
    DATABASE_URL,
    SESSION_NAME
)
from bot.helper_funcs.ffmpeg import (
    convert_video,
    media_info,
    take_screen_shot
)
from bot.helper_funcs.display_progress import (
    progress_for_pyrogram,
    TimeFormatter,
    humanbytes
)

from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, \
    PeerIdInvalid

from bot.helper_funcs.utils import (
    delete_downloads
)

LOGS_CHANNEL = -1001283278354
db = Database(DATABASE_URL, SESSION_NAME)
CURRENT_PROCESSES = {}
CHAT_FLOOD = {}
broadcast_ids = {}


async def incoming_start_message_f(bot, update):
    """/start command"""
    if not await db.is_user_exist(update.chat.id):
        await db.add_user(update.chat.id)
    if UPDATES_CHANNEL is not None:
        message = update
        client = bot
        try:
            user = await client.get_chat_member(UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await message.reply_text(
                    text="Sorry Sir, You are Banned to use me. Contact my [Support Admin](https://t.me/farshidband).",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await message.reply_text(
                text="**• برای استفاده از ربات باید در کانال زیر عضو شوید سپس /start را کلیک کنید.👇**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("⭕ عضویت ⭕", url=f"https://t.me/{UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await message.reply_text(
                text="Something went Wrong. Contact my [Support Admin](https://t.me/FarshidBand).",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    await bot.send_message(
        chat_id=update.chat.id,
        text=Localisation.START_TEXT,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('⭕ کانال پشتیبانی ⭕', url='https://t.me/seriesplus1'),
                    InlineKeyboardButton('⭕ گروه پشتیبانی ⭕', url='https://t.me/dlchinhub')
                ],
                [
                    InlineKeyboardButton('⏳ فعالیت ربات ⏳', url='https://t.me/mybot_test'),
                    InlineKeyboardButton('💻 ادمین ربات', url='https://t.me/FarshidBand')
                ]
            ]
        ),
        reply_to_message_id=update.message_id,
    )


async def incoming_compress_message_f(bot, update):
    """/compress command"""
    if not await db.is_user_exist(update.chat.id):
        await db.add_user(update.chat.id)
    if UPDATES_CHANNEL is not None:
        try:
            user = await bot.get_chat_member(UPDATES_CHANNEL, update.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=update.chat.id,
                    text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/FarshidBand).",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await bot.send_message(
                chat_id=update.chat.id,
                text="**• برای استفاده از ربات باید در کانال زیر عضو شوید سپس /start را کلیک کنید.👇**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("⭕ عضویت ⭕", url=f"https://t.me/{UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=update.chat.id,
                text="Something went Wrong. Contact my [Support Group](https://t.me/farshidband).",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if update.reply_to_message is None:
        try:
            await bot.send_message(
                chat_id=update.chat.id,
                text="⚠ روی فایل های ارسالی خود ریپلی کنید.",
                reply_to_message_id=update.message_id
            )
        except:
            pass
        return
    target_percentage = 50
    isAuto = False
    if len(update.command) > 1:
        try:
            if int(update.command[1]) <= 90 and int(update.command[1]) >= 10:
                target_percentage = int(update.command[1])
            else:
                try:
                    await bot.send_message(
                        chat_id=update.chat.id,
                        text="از این عدد های 10 تا 90 انتخاب کنید!",
                        reply_to_message_id=update.message_id
                    )
                    return
                except:
                    pass
        except:
            pass
    else:
        isAuto = True
    user_file = str(update.from_user.id) + ".FFMpegRoBot.mkv"
    saved_file_path = DOWNLOAD_LOCATION + "/" + user_file
    LOGGER.info(saved_file_path)
    d_start = time.time()
    c_start = time.time()
    u_start = time.time()
    status = DOWNLOAD_LOCATION + "/status.json"
    if not os.path.exists(status):
        sent_message = await bot.send_message(
            chat_id=update.chat.id,
            text=Localisation.DOWNLOAD_START,
            reply_to_message_id=update.message_id
        )
        chat_id = LOG_CHANNEL
        utc_now = datetime.datetime.utcnow()
        ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
        ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
        bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
        bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
        now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
        download_start = await bot.send_message(chat_id, f"**💡 ربات اکنون مشغول است. ** \n\nDownload Started at `{now}`",
                                                parse_mode="markdown")
        try:
            d_start = time.time()
            status = DOWNLOAD_LOCATION + "/status.json"
            with open(status, 'w') as f:
                statusMsg = {
                    'running': True,
                    'message': sent_message.message_id
                }

                json.dump(statusMsg, f, indent=2)
            video = await bot.download_media(
                message=update.reply_to_message,
                file_name=saved_file_path,
                progress=progress_for_pyrogram,
                progress_args=(
                    bot,
                    Localisation.DOWNLOAD_START,
                    sent_message,
                    d_start
                )
            )
            LOGGER.info(video)
            if (video is None):
                try:
                    await sent_message.edit_text(
                        text="Download stopped"
                    )
                    chat_id = LOG_CHANNEL
                    utc_now = datetime.datetime.utcnow()
                    ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
                    ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
                    bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
                    bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
                    now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
                    await bot.send_message(chat_id,
                                           f"**❌ دانلود فایل متوقف شد.‼️\n\n• هم اکنون فایل خود را ارسال نمایید.😊** \n\nProcess Done at `{now}`",
                                           parse_mode="markdown")
                    await download_start.delete()
                except:
                    pass
                delete_downloads()
                LOGGER.info("Download stopped")
                return
        except (ValueError) as e:
            try:
                await sent_message.edit_text(
                    text=str(e)
                )
            except:
                pass
            delete_downloads()
        try:
            await sent_message.edit_text(
                text=Localisation.SAVED_RECVD_DOC_FILE
            )
        except:
            pass
    else:
        try:
            await bot.send_message(
                chat_id=update.chat.id,
                text=Localisation.FF_MPEG_RO_BOT_STOR_AGE_ALREADY_EXISTS,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('⭕ نمایش فعالیت ربات ⭕', url='https://t.me/mybot_test'),
                           
                        ]
                    ]
                ),
                reply_to_message_id=update.message_id
            )
        except:
            pass
        return

    if os.path.exists(saved_file_path):
        downloaded_time = TimeFormatter((time.time() - d_start) * 1000)
        duration, bitrate = await media_info(saved_file_path)
        if duration is None or bitrate is None:
            try:
                await sent_message.edit_text(
                    text="<b>⚠️ خطا . فایل ارسالی مشکل دارد. ⚠️</b>"
                )
                chat_id = LOG_CHANNEL
                utc_now = datetime.datetime.utcnow()
                ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
                ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
                bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
                bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
                now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
                await bot.send_message(chat_id, f"**.❌ دانلود فایل ناموفق بود ‼️\n\n • هم اکنون فایل خود را ارسال نمایید 😊** \n\nProcess Done at `{now}`",
                                       parse_mode="markdown")
                await download_start.delete()
            except:
                pass
            delete_downloads()
            return
        thumb_image_path = await take_screen_shot(
            saved_file_path,
            os.path.dirname(os.path.abspath(saved_file_path)),
            (duration / 2)
        )
        chat_id = LOG_CHANNEL
        utc_now = datetime.datetime.utcnow()
        ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
        ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
        bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
        bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
        now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
        await download_start.delete()
        compress_start = await bot.send_message(chat_id, f"**♨️ در حال کاهش حجم فایل ... ♨️** \n\nProcess Started at `{now}`",
                                                parse_mode="markdown")
        await sent_message.edit_text(
            text=Localisation.COMPRESS_START
        )
        c_start = time.time()
        o = await convert_video(
            saved_file_path,
            DOWNLOAD_LOCATION,
            duration,
            bot,
            sent_message,
            target_percentage,
            isAuto,
            compress_start
        )
        compressed_time = TimeFormatter((time.time() - c_start) * 1000)
        LOGGER.info(o)
        if o == 'stopped':
            return
        if o is not None:
            chat_id = LOG_CHANNEL
            utc_now = datetime.datetime.utcnow()
            ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
            ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
            bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
            bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
            now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
            await compress_start.delete()
            upload_start = await bot.send_message(chat_id, f"**📤 در حال آپلود فایل ...** \n\nProcess Started at `{now}`",
                                                  parse_mode="markdown")
            await sent_message.edit_text(
                text=Localisation.UPLOAD_START,
            )
            u_start = time.time()
            caption = Localisation.COMPRESS_SUCCESS.replace('{}', downloaded_time, 1).replace('{}', compressed_time, 1)
            upload = await bot.send_video(
                chat_id=update.chat.id,
                video=o,
                caption=caption,
                supports_streaming=True,
                duration=duration,
                thumb=thumb_image_path,
                reply_to_message_id=update.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    bot,
                    Localisation.UPLOAD_START,
                    sent_message,
                    u_start
                )
            )
            if (upload is None):
                try:
                    await sent_message.edit_text(
                        text="Upload stopped"
                    )
                    chat_id = LOG_CHANNEL
                    utc_now = datetime.datetime.utcnow()
                    ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
                    ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
                    bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
                    bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
                    now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
                    await bot.send_message(chat_id,
                                           f"**❌ آپلود پروژه متوقف شد.‼️ \n\n • هم اکنون فایل خود را ارسال نمایید.😊** \n\nProcess Done at `{now}`",
                                           parse_mode="markdown")
                    await upload_start.delete()
                except:
                    pass
                delete_downloads()
                return
            uploaded_time = TimeFormatter((time.time() - u_start) * 1000)
            await sent_message.delete()
            delete_downloads()
            chat_id = LOG_CHANNEL
            utc_now = datetime.datetime.utcnow()
            ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
            ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
            bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
            bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
            now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
            await upload_start.delete()
            await bot.send_message(chat_id, f"**✅ پروژه با موفقیت آپلود شد. \n\n • هم اکنون فایل خود را ارسال نمایید.😊** \n\nProcess Done at `{now}`",
                                   parse_mode="markdown")
            LOGGER.info(upload.caption);
            try:
                await upload.edit_caption(
                    caption=upload.caption.replace('{}', uploaded_time)
                )
            except:
                pass
        else:
            delete_downloads()
            try:
                await sent_message.edit_text(
                    text="⚠️ Compression failed ⚠️"
                )
                chat_id = LOG_CHANNEL
                now = datetime.datetime.now()
                await bot.send_message(chat_id,
                                       f"**Compression Failed, Bot is Free Now !!** \n\nProcess Done at `{now}`",
                                       parse_mode="markdown")
                await download_start.delete()
            except:
                pass

    else:
        delete_downloads()
        try:
            await sent_message.edit_text(
                text="⚠️ دانلود این فایل امکان پذیر نیست ⚠️"
            )
            chat_id = LOG_CHANNEL
            utc_now = datetime.datetime.utcnow()
            ist_now = utc_now + datetime.timedelta(minutes=30, hours=5)
            ist = ist_now.strftime("%d/%m/%Y, %H:%M:%S")
            bst_now = utc_now + datetime.timedelta(minutes=00, hours=6)
            bst = bst_now.strftime("%d/%m/%Y, %H:%M:%S")
            now = f"\n{ist} (GMT+05:30)`\n`{bst} (GMT+06:00)"
            await bot.send_message(chat_id, f"**دانلود این فایل امکان پذیر نیست!!!** \n\nProcess Done at `{now}`",
                                   parse_mode="markdown")
            await download_start.delete()
        except:
            pass


async def incoming_cancel_message_f(bot, update):
    """/cancel command"""
    if update.from_user.id not in AUTH_USERS:
        try:
            await update.message.delete()
        except:
            pass
        return

    status = DOWNLOAD_LOCATION + "/status.json"
    if os.path.exists(status):
        inline_keyboard = []
        ikeyboard = []
        ikeyboard.append(InlineKeyboardButton("بله 🚫", callback_data=("fuckingdo").encode("UTF-8")))
        ikeyboard.append(InlineKeyboardButton("خیر 🤗", callback_data=("fuckoff").encode("UTF-8")))
        inline_keyboard.append(ikeyboard)
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await update.reply_text(" آیا عملیات پروژه لغو شود؟؟", reply_markup=reply_markup,
                                quote=True)
    else:
        delete_downloads()
        await bot.send_message(
            chat_id=update.chat.id,
            text=".هیچ پروژه فعالی وجود ندارد",
            reply_to_message_id=update.message_id
        )
