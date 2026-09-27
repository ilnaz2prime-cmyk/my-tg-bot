import os
import time
from telebot import TeleBot
from google import genai
from google.genai import types

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "🎬 Привет! Отправь описание видео на английском языке (например: 'a futuristic car driving in neon rain'), и я сгенерирую его через Omni Flash 1.1.")

@bot.message_handler(func=lambda m: True)
def generate_video(message):
    prompt = message.text
    msg = bot.reply_to(message, "⏳ Отправил запрос в Omni Flash 1.1. Генерация 10-секундного видео занимает около 1-2 минут...")

    try:
        operation = client.models.generate_videos(
            model="gemini-omni-1.1-flash",
            prompt=prompt,
            config=types.GenerateVideosConfig(
                duration_seconds=10,
                aspect_ratio="16:9"
            ),
        )

        while not operation.done:
            time.sleep(10)
            operation = client.operations.get(operation)

        generated_video = operation.result.generated_videos[0]
        client.files.download(file=generated_video.video, path="output.mp4")

        with open("output.mp4", "rb") as video_file:
            bot.send_video(message.chat.id, video_file, caption=f"🎬 {prompt}")

        if os.path.exists("output.mp4"):
            os.remove("output.mp4")

    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка генерации: {e}")

bot.infinity_polling()
