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
# importlib.reload(commands)
from command.commands import (
    link_command,
    button_callback,
)
# from storage.lucostore import client

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')


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
    

# async def main():
#     # Start the client
#     await client.start(bot_token=BOT_TOKEN)
#     logger.info("✅ LucoBOT connected successfully .......")
    
#     # Run until disconnected
#     await client.run_until_disconnected()

if __name__ == "__main__":
    luco_run()
    logger.info("✅ LucoBOT connected successfully .......")
    
    # import asyncio
    # asyncio.run(main())
