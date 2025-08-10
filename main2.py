import pylast as fm
import telebot
from telebot import types
from consts import *
import webbrowser
import requests


bot = telebot.TeleBot(TG_TOKEN)
network = fm.LastFMNetwork(api_key=FM_API_KEY, api_secret=FM_API_SECRET, username=FM_USERNAME)

def create_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("🎧 last song")
    button2 = types.KeyboardButton("🚹 open your profile")
    markup.add(button1, button2)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'choose your action ugly ahh bih', reply_markup=create_keyboard())


@bot.message_handler(content_types=["text"])
def text(message):
    if message.text == "🎧 last song":
        last_track(message)
    elif message.text == "🚹 open your profile":
        webbrowser.open(f"www.last.fm/user/{FM_USERNAME}")
        bot.send_message(message.chat.id, "tryna find your bs")
        
    
@bot.message_handler(commands=["lasttrack"])
def last_track(message):
    user = network.get_user(FM_USERNAME)
    last_track = user.get_recent_tracks(limit=1)[0]
    reply = (
        f"Your last track:\n"
        f"\"{last_track.track.title}\" by {last_track.track.artist.name}\n"
        f"from {last_track.album}"
    )
    
    album = network.get_album(last_track.track.artist.name, last_track.album)
    bot.send_photo(message.chat.id, album.get_cover_image(), caption=reply, reply_markup=create_keyboard())
    
bot.polling(non_stop=True)