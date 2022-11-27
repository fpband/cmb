#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AbirHasan2005

from bot.get_cfg import get_config


class Localisation:
    START_TEXT = "<b>🌟 سلام دوست عزیز خوش آمدید ✨</b> \n\n<b>🔘 من ربات کاربردی کاهش حجم فایل های ویدیویی هستم.</b> \n\n<b>📚 راهنمای ربات ← /help </b> \n\n<b>👤 Admin : @FarshidBand</b>"
   
    ABS_TEXT = " Please don't be selfish."
    
    FORMAT_SELECTION = "Select the desired format: <a href='{}'>file size might be approximate</a> \nIf you want to set custom thumbnail, send photo before or quickly after tapping on any of the below buttons.\nYou can use /deletethumbnail to delete the auto-generated thumbnail."
    
    
    DOWNLOAD_START = "<b>📥 در حال دانلود ... 📥 </b>\n"
    
    UPLOAD_START = "<b>📤 در حال آپلود ... 📤 </b> \n"
    
    COMPRESS_START = "<b>📀 در حال عملیات کم حجم کردن فایل 📀</b>"
    
    RCHD_BOT_API_LIMIT = "size greater than maximum allowed size (50MB). Neverthless, trying to upload."
    
    RCHD_TG_API_LIMIT = "Downloaded in {} seconds.\nDetected File Size: {}\nSorry. But, I cannot upload files greater than 1.95GB due to Telegram API limitations."
    
    COMPRESS_SUCCESS = "📥 مدت زمان دانلود : {}\n\n📀 مدت زمان کاهش حجم فایل : {}\n\n📤 مدت زمان آپلود فایل : {}\n\n<b>⚜️ Admin @FarshidBand </b>"

    COMPRESS_PROGRESS = "⏳ ETA: {}\n🚀 Progress: {}%"

    SAVED_CUSTOM_THUMB_NAIL = "Custom video / file thumbnail saved. This image will be used in the video / file."
    
    DEL_ETED_CUSTOM_THUMB_NAIL = "✅ Custom thumbnail cleared succesfully."
    
    FF_MPEG_DEL_ETED_CUSTOM_MEDIA = "✅ Media cleared succesfully."
    
    SAVED_RECVD_DOC_FILE = "✅ دانلود فایل با موفقیت انجام شد."
    
    CUSTOM_CAPTION_UL_FILE = " "
    
    NO_CUSTOM_THUMB_NAIL_FOUND = "No Custom ThumbNail found."
    
    NO_VOID_FORMAT_FOUND = "no-one gonna help you\n{}"
    
    USER_ADDED_TO_DB = "User <a href='tg://user?id={}'>{}</a> added to {} till {}."
    
    FF_MPEG_RO_BOT_STOR_AGE_ALREADY_EXISTS = "<b>⚠️ ربات در حال انجام کار کاربر دیگری است دقایقی دیگر تلاش کنید ⚠️ </b> \n\n<b>📍نمایش فعالیت ربات 👇.</b>"
    
    HELP_MESSAGE = get_config(
        "STRINGS_HELP_MESSAGE",
        "<b>✵ ابتدا فایل را به این ربات ارسال کنید.</b> \n\n<b>✵ سپس روی فایل ارسالی خود ریپلی کنید.</b> \n\n<b>→  /compress 50  ←</b> \n\n<b>✵ بجای عدد 50 | میزانی که میخواهید کم حجم کنید بنویسید.</b>\n\n<b>📌 تذکر ؛ لطفا فقط از عدد های 10 تا 90 استفاده کنید.</b>"
    )
    WRONG_MESSAGE = get_config(
        "STRINGS_WRONG_MESSAGE",
        "current CHAT ID: <code>{CHAT_ID}</code>"
    )

    
