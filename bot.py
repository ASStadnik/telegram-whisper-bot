import whisper
from pydub import AudioSegment
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

model = whisper.load_model("base")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.voice.get_file()
    await file.download_to_drive("input.ogg")

    audio = AudioSegment.from_ogg("input.ogg")
    audio.export("converted.wav", format="wav")

    result = model.transcribe("converted.wav")
    await update.message.reply_text(result["text"])

import os
TOKEN = os.getenv("BOT_TOKEN")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    print("Бот запущен")
    app.run_polling()
