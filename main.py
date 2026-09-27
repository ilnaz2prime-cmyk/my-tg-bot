import os
import fal_client
from telebot import TeleBot

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
os.environ["FAL_KEY"] = os.getenv("FAL_KEY")

bot = TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "Привет! Отправь мне описание видео на английском языке, и я сгенерирую его через Omni Flash 1.1.")

@bot.message_handler(func=lambda m: True)
def generate(message):
    prompt = message.text
    msg = bot.reply_to(message, "⏳ Создаю видео, это займет около 1–2 минут...")
    try:
        handler = fal_client.submit(
            "fal-ai/omni-flash-1.1",
            arguments={"prompt": prompt, "duration": 10}
        )
        result = handler.get()
        video_url = result['video']['url']
        bot.send_video(message.chat.id, video_url, caption=f"🎬 {prompt}")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

bot.infinity_polling()
