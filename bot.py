
import json
import os
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("8323330293:AAHfCizYsWvUp1A32hDHxKl3kReY8BTF0Qs")

DATA_FILE = "user_data.json"

def save_data(data):
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

    with open(DATA_FILE, "r") as f:
        old_data = json.load(f)

    old_data.append(data)

    with open(DATA_FILE, "w") as f:
        json.dump(old_data, f, indent=4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Send me any message, I will save it.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    data = {
        "user_id": user.id,
        "username": user.username,
        "text": update.message.text,
        "time": datetime.now().isoformat()
    }

    save_data(data)

    await update.message.reply_text("✅ Your message has been saved!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
