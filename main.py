import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests
import validators
import yt_dlp
import os
def is_valid_url(url):
    return validators.url(url)



TOKEN = "6992053959:AAG2EXsgedtaMnltLUWS8dFpqxhdlhsl3SE"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me! Run the command /help for possible commands")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="/image <URL> \n /video <youtube URL>")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


async def get_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_url = context.args[0]
    image_formats = ("image/png", "image/jpeg", "image/jpg", "image/gif", "image/bmp", "image/tiff", "image/webp")
    r = requests.head(image_url)
    if not r.headers["content-type"] in image_formats:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid URL.")
        return
    #if not is_valid_url(image_url):
    #    await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid URL.")
    #    return
    img_data = requests.get(image_url).content
    with open('image.' + image_url.split('.')[-1], 'wb') as handler:
        handler.write(img_data)
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('image.' + image_url.split('.')[-1], 'rb'))


async def get_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video_url = context.args[0]
    if not is_valid_url(video_url):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid URL.")
        return

    ydl_opts = {
        'outtmpl': 'video.mp4',
        'format_sort': ['res:720', 'ext:mp4:m4a']
    }
    try:
        os.remove('video.mp4')
    except OSError:
        pass
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_url)

    await context.bot.send_video(chat_id=update.effective_chat.id,
                                 video=open('video.mp4', 'rb'))

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    image_handler = CommandHandler('image', get_image)
    start_handler = CommandHandler('start', start)
    video_handler = CommandHandler('video', get_video)
    help_handler = CommandHandler('help', help)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(video_handler)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(image_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
