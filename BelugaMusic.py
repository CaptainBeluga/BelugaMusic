from time import *
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
import youtube_dl
import os

TOKEN = "5550360361:AAGzMdR-_QljfEiHEve_WlWSjjSJmO_sYBU"

PATH = "music/"


def start(update,context):
    update.message.reply_text("Welcome to 🐳 BelugaMusic 🐳, you can listen and download music by paste the Youtube URL here !😜")

def answer(update,context):

    songName = update.message.text

    response = requests.get(songName)

    msg = update.message.reply_text("We are searching the song online .....")

    sleep(2.5)

    if response.status_code != 404:
        video_info = youtube_dl.YoutubeDL().extract_info(
            url = songName, download = False
        )

        msg.edit_text(f"Song Name => {video_info['title']}")

        sleep(3)

        try:
            msg.edit_text(f"Music Found Locally !")

            sleep(2)

            msg.edit_text(f"Music Sending => IN PROGRESS .....")
            update.message.reply_document(open(f"{PATH}{video_info['title'].lower()}.mp3","rb"))
            msg.edit_text(f"Music Sending => COMPLETE")

        except:
            options = {
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': f"{PATH}{video_info['title'].lower()}.mp3",
            }

            msg.edit_text(f"Music Download => IN PROGRESS .....")
            
            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([video_info['webpage_url']])
            

            msg.edit_text(f"Music Download => COMPLETE")
            
            sleep(2)

            msg.edit_text("Music Send => IN PROGRESS")

            update.message.reply_document(open(f"{PATH}{video_info['title'].lower()}.mp3","rb"))

            msg.edit_text("Music Send => COMPLETE")
        
        
    else:
        msg.edit_text(f"Link is NOT valid !")

updater = Updater(TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, answer))
print("Beluga Bot is listening.....")
updater.start_polling()
