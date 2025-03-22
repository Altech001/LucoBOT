import logging
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler,CallbackContext, filters, CallbackQueryHandler
from dotenv import load_dotenv

from command.commands import help_command, start_command
from utils.utils import url_link



#================= Menu Button ==================================
def get_menu():
    keyboard = [
        [KeyboardButton("📋LucoBOT Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start_command_with_keyboard(update: Update, context):
    await update.message.reply_text(
        "🛠️ Welcome To LucoBot Ultimate Video Assistant\n\n",
        reply_markup=get_menu()
    )
    await start_command(update, context)

async def help_command_with_keyboard(update: Update, context):
    await update.message.reply_text(
        "💻 *Guidelines and BOT Docs*\n\n",
        reply_markup=get_menu()
    )
    await help_command(update, context)

async def share_command(update: Update, context: CallbackContext) -> None:
    bot_username = context.bot.username
    user = update.effective_user
    share_text = (
        "🎬 *Share LucoBot with your friends!*\n\n"
        f"https://t.me/{bot_username}\n\n"
        "LucoBot - The Ultimate video assistant!"
    )
    
    keyboard = [
        [InlineKeyboardButton("📲 Share BOT", switch_inline_query=f"Yoo, {user.first_name} LucoBOT is awesome!!")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(share_text, parse_mode='Markdown', reply_markup=reply_markup)



async def handle_msg(update: Update, context):
    msg = update.message.text
    user = update.effective_user
    
    if(url_link(msg)):
        update.reply_text("Your link is being analyzed succesfully.")
    
    elif msg == "📋LucoBOT Menu":
        menu_text  = (
        f"{user.first_name} Your Guide !!\n\n"
        "🔹/start   - 👋Starts the LucoBot\n"
        "🔹/help     -  🛠️Displays help dialog\n"
        "🔹/share    - 🚧Shares the bot link\n"
        "🔹/list     -  🎬All Videos & Movies List\n"
        "🔹/link     -  🎬Downloads the shared link\n"
        )
        await update.message.reply_text(menu_text, reply_markup=get_menu())
        return
    else:
        await update.message.reply_text("❌ I don't understand this command. Please use the menu options ⌨️", quote=True)
