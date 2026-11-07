import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from google import genai

# Configuration des logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Récupération des clés depuis les variables d'environnement Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Initialisation du client Google GenAI
client = genai.Client(api_key=GEMINI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bonjour Josh ! Je suis ton assistant IA. Pose-moi n'importe quelle question !")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=user_text,
        )
        reply_text = response.text
    except Exception as e:
        logging.error(f"Erreur Gemini: {e}")
        reply_text = "Désolé, une erreur technique est survenue."
    
    await context.bot.send_message(chat_id=chat_id, text=reply_text)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    await app.initialize()
    await app.start()
    print("Le bot est en route !")
    await app.updater.start_polling()
    
    await asyncio.Event().wait()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
