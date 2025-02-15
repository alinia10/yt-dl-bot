import os
import asyncio
import logging
from telegram import Update
from telegram.ext import ContextTypes
from downloader import download_video
from config import load_config
from log import simple_logger, LoggingLevel
from nextcloud_upload import upload_to_nextcloud

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB limit for Telegram uploads

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me a YouTube video or playlist link to download and upload.")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video_url = update.message.text.strip()
    config = load_config()
    cookies_path = 'cookies.txt'  # Ensure this file exists and has valid YouTube cookies.
    simple_logger(f"Received URL: {video_url}")

    await update.message.reply_text("Downloading video(s)...")
    try:
        # Download all videos (playlist or single video).
        files = await asyncio.to_thread(download_video, video_url, cookies_path)
        await update.message.reply_text(f"Downloaded {len(files)} video(s). Processing each file...")

        # Process each downloaded file.
        for file_path in files:
            file_size = os.path.getsize(file_path)
            if file_size > MAX_FILE_SIZE:
                await update.message.reply_text("File is too large for Telegram. Uploading to Nextcloud...")
                share_link = await asyncio.to_thread(upload_to_nextcloud, file_path, config)
                await update.message.reply_text(f"File uploaded to Nextcloud:\n{share_link}")
            else:
                await update.message.reply_text("Uploading video to Telegram...")
                with open(file_path, 'rb') as video_file:
                    await update.message.reply_document(document=video_file)
            os.remove(file_path)
        await update.message.reply_text("All videos processed and removed from server.")
        simple_logger("Download and processing completed successfully.")
    except Exception as e:
        error_msg = f"Error: {e}"
        await update.message.reply_text(error_msg)
        simple_logger(error_msg, log_level=logging.ERROR)
