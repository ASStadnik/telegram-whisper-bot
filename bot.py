import os
import whisper
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Указываем путь к ffmpeg для всех, кто его ищет
os.environ["PATH"] += os.pathsep + "C:/ProgramData/chocolatey/bin"

# Загружаем модель Whisper
# model = whisper.load_model("base")
model = whisper.load_model("tiny")

# Обработка голосовых сообщений
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.voice.get_file()
    await file.download_to_drive("input.ogg")

    # Конвертация .ogg в .wav
    subprocess.run([
        "ffmpeg", "-y", "-i", "input.ogg", "converted.wav"
    ], check=True)

    # Распознавание речи
    result = model.transcribe("converted.wav")
    await update.message.reply_text(result["text"])

# Токен Telegram-бота
TOKEN = "7616672879:AAGnj3gd5R1eSS4UA6zEj2JfMdD5ZWBMCE8"

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    print("Бот запущен")
    app.run_polling()
