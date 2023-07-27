import telebot
import os
from pytube import YouTube


bot = telebot.TeleBot('6609303080:AAGQo3nWUd7RfGipLM21SPlD_RgDe8odavI')


VIDEO, AUDIO, BOTH = range(3)


@bot.message_handler(commands=['start', 'command1'])
def start(message):
    bot.reply_to(message, "Send me a YouTube link, and I'll download it as video, audio, or both!")
    bot.register_next_step_handler(message, receive_link)


def receive_link(message):
    url = message.text.strip()
    try:
        youtube_video = YouTube(url)
        title = youtube_video.title


        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add(telebot.types.KeyboardButton("Video"))
        keyboard.add(telebot.types.KeyboardButton("Audio"))
        keyboard.add(telebot.types.KeyboardButton("Both"))

        bot.reply_to(message, f"Title: {title}\nChoose the format:", reply_markup=keyboard)


        bot.register_next_step_handler(message, receive_choice, youtube_video)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")


def receive_choice(message, youtube_video):
    choice = message.text.strip()

    if choice == 'Video':
        file_path = youtube_video.streams.get_highest_resolution().download()
        bot.reply_to(message, "Downloading video...")
        bot.send_video(message.chat.id, open(file_path, 'rb'))
        os.remove(file_path)
    elif choice == 'Audio':
        file_path = youtube_video.streams.filter(only_audio=True).first().download()
        bot.reply_to(message, "Downloading audio...")
        bot.send_audio(message.chat.id, open(file_path, 'rb'))
        os.remove(file_path)
    elif choice == 'Both':
        video_file_path = youtube_video.streams.get_highest_resolution().download()
        audio_file_path = youtube_video.streams.filter(only_audio=True).first().download()

        bot.reply_to(message, "Downloading video...")
        bot.send_video(message.chat.id, open(video_file_path, 'rb'))
        bot.reply_to(message, "Downloading audio...")
        bot.send_audio(message.chat.id, open(audio_file_path, 'rb'))


bot.polling()
