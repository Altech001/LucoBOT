# #======== All instances and Initialization =======

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

# # importlib.reload(commands)
# from command.commands import (
#     link_command,
#     button_callback,
# )

# load_dotenv()

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO)
# logger = logging.getLogger(__name__)

# BOT_TOKEN = os.getenv('BOT_TOKEN')
# PORT = int(os.environ.get("PORT", 8080))

# # Create a Flask web server
# app = Flask(__name__)

# @app.route('/')
# def index():
#     return "Telegram Bot is running!"

# @app.route('/health')
# def health():
#     return "OK"

# def run_flask():
#     # Run Flask on the PORT specified by Render
#     app.run(host='0.0.0.0', port=PORT)

# def luco_run():
#     application = Application.builder().token(BOT_TOKEN).persistence(None).build()
    
#     #=================== Commands =====================================
#     application.add_handler(CommandHandler("start", start_command_with_keyboard))
#     application.add_handler(CommandHandler("help", help_command_with_keyboard))
#     application.add_handler(CommandHandler("share", share_command))
#     application.add_handler(CommandHandler("link", link_command))
    
#     application.add_handler(CallbackQueryHandler(button_callback))
#     # application.add_handler(CallbackQueryHandler(button_callback))
    
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    
#     #=================== Commands End ========================================
    
#     application.run_polling(allowed_updates=Update.ALL_TYPES)

# if __name__ == "__main__":
#     # Start Flask server in a separate thread
#     flask_thread = threading.Thread(target=run_flask)
#     flask_thread.daemon = True  # This ensures the thread will exit when the main program exits
#     flask_thread.start()
    
#     # Start the Telegram bot
#     luco_run()
#     logger.info("✅ LucoBOT connected successfully .......")
# ======== All instances and Initialization =======
# import re
# import logging
# import os
# from command import commands
# from function.menu import handle_msg, help_command_with_keyboard, share_command, start_command_with_keyboard
# from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
# from dotenv import load_dotenv
# from flask import Flask, request

# Import commands
import logging
import os
from command.commands import link_command, button_callback
from function.menu import handle_msg, help_command_with_keyboard, share_command, start_command_with_keyboard
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from dotenv import load_dotenv
from flask import Flask, request

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# Get environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
PORT = int(os.environ.get("PORT", 8080))

# Create a Flask web server
app = Flask(__name__)

# Basic route for health checks
@app.route('/')
def index():
    return "Telegram Bot is running!"

@app.route('/health')
def health():
    return "OK"

# Webhook endpoint for Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    # Initialize application inside the function to avoid scope issues
    application = create_application()
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.process_update(update)
    return 'OK'

def create_application():
    # Create and configure the application
    application = Application.builder().token(BOT_TOKEN).persistence(None).build()
    
    # Set up command handlers
    application.add_handler(CommandHandler("start", start_command_with_keyboard))
    application.add_handler(CommandHandler("help", help_command_with_keyboard))
    application.add_handler(CommandHandler("share", share_command))
    application.add_handler(CommandHandler("link", link_command))
    
    # Callback query handler
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Message handler - handles regular text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    
    return application

if __name__ == "__main__":
    application = create_application()
    
    # Check if running on Render
    if 'RENDER' in os.environ:
        # Get the external URL from Render
        WEBHOOK_URL = os.environ.get('RENDER_EXTERNAL_URL') + '/webhook'
        
        # Set webhook
        application.bot.set_webhook(WEBHOOK_URL)
        logger.info(f"Setting webhook to {WEBHOOK_URL}")
        
        # Run Flask app
        logger.info(f"✅ LucoBOT starting in webhook mode on port {PORT}")
        app.run(host='0.0.0.0', port=PORT)
    else:
        # Local development - use polling
        logger.info("Starting bot in polling mode for local development")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        logger.info("✅ LucoBOT connected successfully in polling mode .......")