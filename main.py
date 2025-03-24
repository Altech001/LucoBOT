# #======== All instances and Initialization =======

# import importlib
# import re
# import logging
# import os
# from command import commands
# from function.menu import handle_msg, help_command_with_keyboard, share_command, start_command_with_keyboard
# from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
# from dotenv import load_dotenv
# import threading
# from flask import Flask, request

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
import importlib
import re
import logging
import os
import asyncio
from command import commands
from function.menu import handle_msg, help_command_with_keyboard, share_command, start_command_with_keyboard
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from dotenv import load_dotenv
import threading
from fastapi import FastAPI, BackgroundTasks
import uvicorn
from fastapi.responses import PlainTextResponse
from functools import wraps, partial

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

# Create a FastAPI app
app = FastAPI()

# Background tasks store
background_tasks = set()

# Decorator for creating repeating tasks
def repeat(interval_seconds):
    def decorator(func):
        @wraps(func)
        async def wrapped_func(*args, **kwargs):
            while True:
                try:
                    await func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error in repeating task: {e}")
                await asyncio.sleep(interval_seconds)
        return wrapped_func
    return decorator

# Repeating task to keep the service active
@repeat(5)
async def keep_alive():
    logger.info("🔄 Keep-alive task running...")
    # You can add additional logic here if needed

@app.on_event("startup")
async def startup_event():
    # Start the keep-alive task
    task = asyncio.create_task(keep_alive())
    # Store the task to prevent it from being garbage collected
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
    
    # Start the Telegram bot in a separate thread
    bot_thread = threading.Thread(target=luco_run)
    bot_thread.daemon = True
    bot_thread.start()
    logger.info("🚀 FastAPI server and Telegram bot started")

@app.get("/", response_class=PlainTextResponse)
async def index():
    return "Telegram Bot is running!"

@app.get("/health", response_class=PlainTextResponse)
async def health():
    return "OK"

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
    # Run FastAPI with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
# # ======== All instances and Initialization =======
# # import re
# # import logging
# # import os
# # from command import commands
# # from function.menu import handle_msg, help_command_with_keyboard, share_command, start_command_with_keyboard
# # from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
# # from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
# # from dotenv import load_dotenv
# # from flask import Flask, request

# # Import commands
# from command.commands import (
#     link_command,
#     button_callback,
# )

# # Load environment variables
# load_dotenv()

# # Configure logging
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Get environment variables
# BOT_TOKEN = os.getenv('BOT_TOKEN')
# PORT = int(os.environ.get("PORT", 8080))

# # Create a Flask web server
# app = Flask(__name__)

# # Initialize Telegram bot application
# application = Application.builder().token(BOT_TOKEN).persistence(None).build()

# # Basic route for health checks
# @app.route('/')
# def index():
#     return "Telegram Bot is running!"

# @app.route('/health')
# def health():
#     return "OK"

# # Webhook endpoint for Telegram
# @app.route('/webhook', methods=['POST'])
# def webhook():
#     update = Update.de_json(request.get_json(force=True), application.bot)
#     application.process_update(update)
#     return 'OK'

# # Set up command handlers
# def setup_handlers():
#     # Commands
#     application.add_handler(CommandHandler("start", start_command_with_keyboard))
#     application.add_handler(CommandHandler("help", help_command_with_keyboard))
#     application.add_handler(CommandHandler("share", share_command))
#     application.add_handler(CommandHandler("link", link_command))
    
#     # Callback query handler
#     application.add_handler(CallbackQueryHandler(button_callback))
    
#     # Message handler - handles regular text messages
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    
#     logger.info("All handlers have been set up")

# if __name__ == "__main__":
#     # Set up handlers
#     setup_handlers()
    
#     # Check if running on Render
#     if 'RENDER' in os.environ:
#         # Get the external URL from Render
#         WEBHOOK_URL = os.environ.get('RENDER_EXTERNAL_URL', f'https://{os.environ.get("RENDER_SERVICE_NAME")}.onrender.com') + '/webhook'
        
#         # Set webhook
#         application.bot.set_webhook(WEBHOOK_URL)
#         logger.info(f"Setting webhook to {WEBHOOK_URL}")
        
#         # Run Flask app
#         logger.info(f"✅ LucoBOT starting in webhook mode on port {PORT}")
#         app.run(host='0.0.0.0', port=PORT)
#     else:
#         # Local development - use polling
#         logger.info("Starting bot in polling mode for local development")
#         application.run_polling(allowed_updates=Update.ALL_TYPES)
#         logger.info("✅ LucoBOT connected successfully in polling mode .......")