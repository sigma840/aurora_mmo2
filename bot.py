import os
from telegram.ext import ApplicationBuilder, CommandHandler

print("START BOT")

TOKEN = os.getenv("TOKEN")
print("TOKEN:", TOKEN)

async def start(update, context):
    await update.message.reply_text("BOT OK")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("RUNNING")
app.run_polling()
