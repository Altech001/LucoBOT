#============================= BOT Commands ===========================================
# /start -> Welcome To LucoBot Ultimate Video Assisstant
# /search -> Looks for the specific video across and place if in db or groups available
# /list -> Lists all the movies in the coverage
# /upload -> Uploads the video to the storage 
# /help -> Lists all the services offered
# /share -> Shares the video url to platform
# /link -> Downloads and Video when a link is pasted in the input
# /tools -> Lists all the tools for anything. Upgrade Incase the bot gets recognized.
#========================================================================

import asyncio
import os
import traceback
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
from dotenv import load_dotenv
import logging
import re




logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

load_dotenv()

async def start_command(update: Update,context: CallbackContext) -> None:
    bot_user = update.effective_user
    msg = (
        "🛠️ Welcome To LucoBot Ultimate Video Assistant\n\n"
        f"🚧 Hello,👋 {bot_user.first_name}!! \n"
        "⚙️ Use /help to see all available commands.\n"
    )
    keyboard = [
        [
            InlineKeyboardButton("Help", callback_data="help"),
            InlineKeyboardButton("Services", callback_data="service"),
        ],
        [
            InlineKeyboardButton("Cloud Storage API", callback_data="store"),
            InlineKeyboardButton("Customer Care", callback_data="cstcare"),
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(msg,parse_mode="Markdown",reply_markup=reply_markup)


async def help_command(update:Update, callback_data: CallbackContext):
    help_msg=(
        "💻 *Guidelines and BOT Docs*\n\n"
        "1. /upload - 🎬Videos upload cloud storage\n"
        "2. /list - 📋List available videos\n"
        "3. /search - 🔍Search videos around the cloud\n"
        "4. /storage - 📌Create an api for your videos and photos\n\n"
        "LucoBot /more on {/www.luco.dev} or +256-708215305\n"
    )
    await update.message.reply_text(help_msg, parse_mode="Markdown")

   
   
async def link_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass  

#================================================================================     
async def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    
    if callback_data == 'help':
        await help_command(update, context)
    elif callback_data.startswith('download_'):
        video_id = callback_data.split('_')[1]
        await query.edit_message_text(f"⏳ Preparing to download video {video_id}...")
        # Implement the actual download logic here
    elif callback_data.startswith('redownload_'):
        video_id = callback_data.split('_')[1]
        await query.edit_message_text(f"⏳ Preparing to re-download video {video_id}...")
        # Implement the re-download logic here
    elif callback_data == 'settings':
        
        keyboard = [
            [
                InlineKeyboardButton("🔍 QUALITY", callback_data='quality_360'),
                InlineKeyboardButton("📱 SERVICES", callback_data='quality_720')
            ],
            [
                InlineKeyboardButton("💻 STORAGE", callback_data='quality_1080'),
                InlineKeyboardButton("🔙 CUSTOMER HELP", callback_data='tools')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("⚙️ Select preferred video quality:", reply_markup=reply_markup)
    elif callback_data.startswith('quality_'):
        quality = callback_data.split('_')[1]
        await query.edit_message_text(f"✅ Quality preference updated to {quality}p")
    elif callback_data.startswith("amount"):
        await query.edit_message_text("List <-> Download 20 videos per-parse")
        

