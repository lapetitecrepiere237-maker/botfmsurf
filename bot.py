import asyncio
import logging
import os
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Configuration
BOT_TOKEN = "8792104899:AAFJGCuj7MzZY-FvMsQ7P9mxlzkngKV6Z4c"
CHANNEL_ID = "@fmsurf1"
HATUNNEL_FILE_PATH = "mtn_hatunnel.hat"

# Activation des logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Serveur Flask pour garder Railway éveillé
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Le bot FMSURF est actif et en ligne !"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host="0.0.0.0", port=port)

# Logique du Bot Telegram
async def handle_new_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post
    
    if message and message.document:
        filename = message.document.file_name or ""
        logging.info(f"Nouveau fichier détecté dans le canal : {filename}")
        
        # Attente de 3 heures 30 minutes (12600 secondes)
        await asyncio.sleep(12600)
        
        alert_text = (
            "⚠️ **ATTENTION : EXPIRATION IMMINENTE !**\n\n"
            "Le fichier Dark Tunnel Orange va expirer dans **30 minutes**.\n"
            "Le prochain fichier Orange sera envoyé à l'heure habituelle.\n\n"
            "🔄 *En attendant, utilisez le fichier Hatunnel MTN ci-dessous pour rester connecté !*"
        )
        
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=alert_text,
            parse_mode="Markdown"
        )
        
        try:
            with open(HATUNNEL_FILE_PATH, "rb") as file:
                await context.bot.send_document(
                    chat_id=CHANNEL_ID,
                    document=file,
                    caption="📂 **Fichier de secours MTN Hatunnel** (Gratuit)"
                )
            logging.info("Alerte et fichier Hatunnel MTN envoyés avec succès !")
        except FileNotFoundError:
            logging.error(f"Fichier de secours introuvable à l'emplacement : {HATUNNEL_FILE_PATH}")

def main():
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.Chat(chat_id=CHANNEL_ID) & filters.Document.ALL, handle_new_file))

    logging.info("Le robot FMSURF est en cours d'exécution...")
    app.run_polling()

if __name__ == "__main__":
    main()
