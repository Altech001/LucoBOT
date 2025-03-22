#======== All instances and Initialization =======

# import importlib
import re
import logging
import os
from command import commands
from function.menu import handle_msg, help_command_with_keyboard, share_command, start_command_with_keyboard
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from dotenv import load_dotenv
import threading
from flask import Flask, request

# importlib.reload(commands)
from command.commands import (
    link_command,
    button_callback,
)

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
PORT = int(os.environ.get("PORT", 8080))

# Create a Flask web server
app = Flask(__name__)

@app.route('/')
def index():
    return "Telegram Bot is running!"

@app.route('/health')
def health():
    return "OK"

def run_flask():
    # Run Flask on the PORT specified by Render
    app.run(host='0.0.0.0', port=PORT)

def luco_run():
    application = Application.builder().token(BOT_TOKEN).persistence(None).build()
    
    #=================== Commands =====================================
    application.add_handler(CommandHandler("start", start_command_with_keyboard))
    application.add_handler(CommandHandler("help", help_command_with_keyboard))
    application.add_handler(CommandHandler("share", share_command))
    application.add_handler(CommandHandler("link", link_command))
    
    application.add_handler(CallbackQueryHandler(button_callback))
    # application.add_handler(CallbackQueryHandler(button_callback))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    
    #=================== Commands End ========================================
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # This ensures the thread will exit when the main program exits
    flask_thread.start()
    
    # Start the Telegram bot
    luco_run()
    logger.info("✅ LucoBOT connected successfully .......")