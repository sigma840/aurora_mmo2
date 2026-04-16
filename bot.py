import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import game

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌆 GTA MMO Aurora online!\n/cmd para comandos")

async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(game.cmd())

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text
    await update.message.reply_text(game.process(uid, text))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("cmd", cmd))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
