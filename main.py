import aiohttp
from consts import *
import requests as rqst
from telegram import Update
from telegram.ext import Application, Updater, CommandHandler, CallbackContext, ContextTypes

TELEGRAM_TOKEN = TG_TOKEN
LAST_FM_API_KEY = FM_API_KEY
LAST_FM_USERNAME = FM_API_USERNAME

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Just a simple command to check'''
    await update.message.reply_text(' dont be nerd stop checking this bs')

async def last_track(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={LAST_FM_USERNAME}&api_key={LAST_FM_API_KEY}&format=json&limit=1"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                
                if "error" in data:
                    await update.message.reply_text(f"Error: {data['message']}")
                    return
                
                last_track_data = data["recenttracks"]["track"][0]
                artist = last_track_data["artist"]["#text"]
                track = last_track_data["name"]
                album = last_track_data["album"]["#text"]
                
                cover_url = None
                if 'image' in last_track_data:
                    for image in last_track_data['image']:
                        if image['size'] == 'extralarge':
                            cover_url = image['#text']
                            break
                    if not cover_url and last_track_data['image']:
                        cover_url = last_track_data['image'][-1]['#text']
                
                message = (
                    f"Last scrobble:\n"
                    f"▶️ {artist} - {track}\n"
                    f"💿 Album: {album}"
                )
                
                if cover_url:
                    await update.message.reply_photo(cover_url, caption=message)
                else:
                    await update.message.reply_text(message)
    
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("lasttrack", last_track))

    application.run_polling()

if __name__ == "__main__":
    main()     
        