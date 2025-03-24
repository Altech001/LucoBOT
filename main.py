# #======== All instances and Initialization =======
# import importlib
# import re
# import logging
# import os
# import asyncio
# import signal
# import sys
# from command import commands
# from function.menu import handle_msg, help_command_with_keyboard, share_command, start_command_with_keyboard
# from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
# from dotenv import load_dotenv
# from fastapi import FastAPI
# import uvicorn
# from fastapi.responses import PlainTextResponse
# import multiprocessing
# from functools import wraps

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

# # Create a FastAPI app
# app = FastAPI()

# # Decorator for creating repeating tasks
# def repeat(interval_seconds):
#     def decorator(func):
#         @wraps(func)
#         async def wrapped_func(*args, **kwargs):
#             while True:
#                 try:
#                     await func(*args, **kwargs)
#                 except Exception as e:
#                     logger.error(f"Error in repeating task: {e}")
#                 await asyncio.sleep(interval_seconds)
#         return wrapped_func
#     return decorator

# # Repeating task to keep the service active
# @repeat(5)
# async def keep_alive():
#     logger.info("🔄 FastAPI keep-alive task running...")
#     # You can add additional logic here if needed

# # Define telegram bot process function
# def run_telegram_bot():
#     # This is run in a separate process with its own event loop
#     logging.basicConfig(
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#         level=logging.INFO)
    
#     logger.info("Starting Telegram bot process...")
    
#     # Define the main async function to run the bot
#     async def main():
#         # Initialize the application
#         application = Application.builder().token(BOT_TOKEN).persistence(None).build()
        
#         #=================== Commands =====================================
#         application.add_handler(CommandHandler("start", start_command_with_keyboard))
#         application.add_handler(CommandHandler("help", help_command_with_keyboard))
#         application.add_handler(CommandHandler("share", share_command))
#         application.add_handler(CommandHandler("link", link_command))
        
#         application.add_handler(CallbackQueryHandler(button_callback))
        
#         application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
#         #=================== Commands End ========================================
        
#         # Start polling
#         await application.initialize()
#         await application.start()
        
#         logger.info("✅ LucoBOT connected successfully .......")
        
#         # Set up graceful shutdown
#         stop_signal = asyncio.Future()
        
#         def signal_handler(sig, frame):
#             logger.info("Received signal to terminate bot...")
#             stop_signal.set_result(True)
        
#         # Register signal handlers
#         for sig in (signal.SIGINT, signal.SIGTERM):
#             signal.signal(sig, signal_handler)
        
#         # Run the bot until stopped
#         await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        
#         try:
#             # Wait until stop signal
#             await stop_signal
#         finally:
#             # Stop the bot gracefully
#             await application.stop()
#             await application.shutdown()
    
#     # Run the event loop
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         logger.info("Telegram bot process terminated by user")
#     except Exception as e:
#         logger.error(f"Error in telegram bot process: {e}")

# # Store background tasks
# background_tasks = set()

# @app.on_event("startup")
# async def startup_event():
#     # Start the keep_alive task
#     task = asyncio.create_task(keep_alive())
#     background_tasks.add(task)
#     task.add_done_callback(lambda t: background_tasks.remove(t) if t in background_tasks else None)
    
#     # Start the Telegram bot in a separate process
#     # This completely isolates the event loops
#     bot_process = multiprocessing.Process(target=run_telegram_bot)
#     bot_process.daemon = True  # Process will terminate when main process exits
#     bot_process.start()
    
#     logger.info(f"🚀 FastAPI server started, Telegram bot running in process {bot_process.pid}")

# @app.get("/", response_class=PlainTextResponse)
# async def index():
#     return "Telegram Bot is running!"

# @app.get("/health", response_class=PlainTextResponse)
# async def health():
#     return "OK"

# if __name__ == "__main__":
#     # Run FastAPI with uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=PORT)

import importlib
import re
import logging
import os
import asyncio
import signal
import sys
import time
from command import commands
from function.menu import handle_msg, help_command_with_keyboard, share_command, start_command_with_keyboard
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from fastapi.responses import PlainTextResponse
import multiprocessing
from functools import wraps

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

# Define a more robust keep-alive decorator with error handling and recovery
def repeat_with_recovery(interval_seconds, max_retries=3, retry_delay=5):
    def decorator(func):
        @wraps(func)
        async def wrapped_func(*args, **kwargs):
            consecutive_failures = 0
            
            while True:
                try:
                    # Run the function and reset failure counter on success
                    await func(*args, **kwargs)
                    consecutive_failures = 0
                except Exception as e:
                    consecutive_failures += 1
                    logger.error(f"Error in repeating task (attempt {consecutive_failures}): {e}")
                    
                    if consecutive_failures >= max_retries:
                        logger.critical(f"Task failed {max_retries} times consecutively. Waiting longer before retry.")
                        # Wait longer before retrying after multiple failures
                        await asyncio.sleep(retry_delay * 2)
                        consecutive_failures = 0  # Reset counter and try again
                    else:
                        # Wait normal interval before retrying
                        pass
                
                # Wait for the next iteration
                await asyncio.sleep(interval_seconds)
        return wrapped_func
    return decorator

# Enhanced keep-alive task with status checking
@repeat_with_recovery(5, max_retries=5, retry_delay=10)
async def keep_alive():
    logger.info("🔄 FastAPI keep-alive task running...")
    
    # Check if the bot process is still running
    bot_status = "Running" if bot_process and bot_process.is_alive() else "Not running"
    logger.info(f"Bot status: {bot_status}")
    
    # Add any additional health checks here
    # For example, you could ping your Telegram bot API to make sure it's responsive

# Define telegram bot process function with automatic recovery
def run_telegram_bot():
    # This is run in a separate process with its own event loop
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    
    logger.info("Starting Telegram bot process...")
    
    # Define the main async function to run the bot
    async def main():
        # Initialize the application
        application = Application.builder().token(BOT_TOKEN).persistence(None).build()
        
        #=================== Commands =====================================
        application.add_handler(CommandHandler("start", start_command_with_keyboard))
        application.add_handler(CommandHandler("help", help_command_with_keyboard))
        application.add_handler(CommandHandler("share", share_command))
        application.add_handler(CommandHandler("link", link_command))
        
        application.add_handler(CallbackQueryHandler(button_callback))
        
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
        #=================== Commands End ========================================
        
        # Start polling
        await application.initialize()
        await application.start()
        
        logger.info("✅ LucoBOT connected successfully .......")
        
        # Set up graceful shutdown
        stop_signal = asyncio.Future()
        
        def signal_handler(sig, frame):
            logger.info("Received signal to terminate bot...")
            stop_signal.set_result(True)
        
        # Register signal handlers
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, signal_handler)
        
        # Run the bot until stopped with error recovery
        await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        
        # Implement a periodic health check within the bot process too
        async def bot_health_check():
            while True:
                try:
                    # Log that the bot is still alive
                    logger.info("Bot health check: Bot is running")
                    # Could add additional checks here like testing a command
                    await asyncio.sleep(30)  # Check every 30 seconds
                except Exception as e:
                    logger.error(f"Error in bot health check: {e}")
                    await asyncio.sleep(5)  # Shorter retry interval if health check fails
        
        # Start the health check as a background task
        health_check_task = asyncio.create_task(bot_health_check())
        
        try:
            # Wait until stop signal
            await stop_signal
        finally:
            # Stop the bot gracefully
            health_check_task.cancel()
            await application.stop()
            await application.shutdown()
    
    # Run the event loop with auto-restart capability
    restart_attempts = 0
    max_restarts = 10
    restart_delay = 5
    
    while restart_attempts < max_restarts:
        try:
            asyncio.run(main())
            # If we get here without exception, it was a clean shutdown
            logger.info("Telegram bot process terminated cleanly")
            break
        except KeyboardInterrupt:
            logger.info("Telegram bot process terminated by user")
            break
        except Exception as e:
            restart_attempts += 1
            logger.error(f"Error in telegram bot process (attempt {restart_attempts}/{max_restarts}): {e}")
            if restart_attempts < max_restarts:
                logger.info(f"Restarting bot in {restart_delay} seconds...")
                time.sleep(restart_delay)
                # Increase delay for next restart to prevent rapid cycling
                restart_delay = min(restart_delay * 2, 60)  # Max 60 seconds between restarts
            else:
                logger.critical(f"Bot failed to restart after {max_restarts} attempts. Giving up.")
                break

# Store background tasks and process reference
background_tasks = set()
bot_process = None

# Function to restart the bot if it crashes
async def monitor_bot_process():
    global bot_process
    
    while True:
        try:
            if bot_process and not bot_process.is_alive():
                logger.warning("Bot process has died. Restarting...")
                # Start a new process
                bot_process = multiprocessing.Process(target=run_telegram_bot)
                bot_process.daemon = True
                bot_process.start()
                logger.info(f"Bot restarted in process {bot_process.pid}")
        except Exception as e:
            logger.error(f"Error in bot process monitor: {e}")
        
        await asyncio.sleep(15)  # Check every 15 seconds

@app.on_event("startup")
async def startup_event():
    global bot_process
    
    # Start the keep_alive task
    keep_alive_task = asyncio.create_task(keep_alive())
    background_tasks.add(keep_alive_task)
    keep_alive_task.add_done_callback(lambda t: background_tasks.remove(t) if t in background_tasks else None)
    
    # Start the bot process monitor
    monitor_task = asyncio.create_task(monitor_bot_process())
    background_tasks.add(monitor_task)
    monitor_task.add_done_callback(lambda t: background_tasks.remove(t) if t in background_tasks else None)
    
    # Start the Telegram bot in a separate process
    bot_process = multiprocessing.Process(target=run_telegram_bot)
    bot_process.daemon = True  # Process will terminate when main process exits
    bot_process.start()
    
    logger.info(f"🚀 FastAPI server started, Telegram bot running in process {bot_process.pid}")

@app.get("/", response_class=PlainTextResponse)
async def index():
    # Include bot status in response
    bot_status = "running" if bot_process and bot_process.is_alive() else "not running"
    return f"Telegram Bot is {bot_status}!"

@app.get("/health", response_class=PlainTextResponse)
async def health():
    # More detailed health check
    if bot_process and bot_process.is_alive():
        return "OK - Bot process is running"
    else:
        return "WARNING - Bot process is not running"

if __name__ == "__main__":
    # Run FastAPI with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)