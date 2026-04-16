import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

print("🚀 BOT A ARRANCAR...")

TOKEN = os.getenv("TOKEN")

print("🔑 TOKEN =", TOKEN)

# ❌ NÃO importar game ainda (teste)
# import game


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌆 BOT ONLINE (DEBUG MODE)")

async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("CMD FUNCIONA (sem game ainda)")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("BOT RESPONDE OK (sem game ainda)")


print("⚙️ A criar aplicação...")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("cmd", cmd))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("▶️ A INICIAR BOT...")

app.run_polling()
