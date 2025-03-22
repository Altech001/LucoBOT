# command/list_commands.py - New file for list and download commands
from telegram import Update
from telegram.ext import ContextTypes
import asyncio
import logging
from storage.lucostore import get_videos_from_bucket, download_video_by_id, telethon_client

logger = logging.getLogger(__name__)

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command to list all videos from the Bucket group"""
    message = await update.message.reply_text("Fetching videos from LucoCloud... Please wait.")
    
    # Get videos using telethon client
    videos = await get_videos_from_bucket()
    
    if isinstance(videos, dict) and "error" in videos:
        await message.edit_text(f"Error: {videos['error']}")
        return
    
    if not videos:
        await message.edit_text("The LucoCloud is currently empty 🙁")
        return
    
    # Format the response with video list
    response = "📹 **Available Videos in Bucket** 📹\n\n"
    for i, video in enumerate(videos, 1):
        response += f"{i}. **{video['title']}**\n"
        response += f"   - Size: {video['size']}\n"
        response += f"   - Date: {video['date']}\n"
        response += f"   - Caption: {video['caption']}\n"
        response += f"   - Tap Download link: /download_{video['id']}\n\n"
    
    await message.edit_text(response, parse_mode="Markdown")

async def download_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command to download a specific video by its message ID"""
    # Check if the command has correct format
    text = update.message.text
    import re
    match = re.match(r'/download_(\d+)', text)
    
    if not match:
        await update.message.reply_text("Invalid download command. Use /download_ID")
        return
    
    message_id = int(match.group(1))
    status_message = await update.message.reply_text(f"Downloading video... Please wait.")
    
    # Get video using telethon client
    video_data = await download_video_by_id(message_id)
    
    if isinstance(video_data, dict) and "error" in video_data:
        await status_message.edit_text(f"Error: {video_data['error']}")
        return
    
    # Send the video
    await status_message.edit_text(f"Sending video: {video_data['title']}")
    
    # We need to use telethon to send the file to the Telegram chat
    chat_id = update.effective_chat.id
    await telethon_client.send_file(
        chat_id, 
        video_data["message"].media, 
        caption=video_data["caption"]
    )
    
    await status_message.delete()