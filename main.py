import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

SHORTENER_DOMAINS = [
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "shorte.st", "adf.ly", 
    "is.gd", "buff.ly", "ow.ly", "cutt.ly", "rebrand.ly"
]

def expand_url(short_url: str) -> str:
    try:
        response = requests.head(short_url, allow_redirects=True, timeout=10)
        return response.url if response.status_code == 200 else "Invalid or inaccessible URL."
    except Exception as e:
        return f"Error: {str(e)}"

def is_shortened_url(url: str) -> bool:
    for domain in SHORTENER_DOMAINS:
        if domain in url:
            return True
    return False

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("👋 Welcome! Send me any shortened URL, and I'll expand it for you.")

def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text.strip()
    if user_message.startswith("http://") or user_message.startswith("https://"):
        if is_shortened_url(user_message):
            expanded_url = expand_url(user_message)
            update.message.reply_text(f"🔗 Expanded URL: {expanded_url}")
        else:
            update.message.reply_text("❌ This doesn't seem to be a shortened URL.")
    else:
        update.message.reply_text("❌ Please send a valid URL.")

def main():
    bot_token = "7118301882:AAFuroSozOSAkgNYSaVCWUqEvawkQFlE4to"
    updater = Updater(token=bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
