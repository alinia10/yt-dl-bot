import os
import logging
from telegram import Update
from telegram.ext import CallbackContext
from downloader import download_video
from config import load_config
from log import simple_logger

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi! Send me a YouTube video or playlist link to download and upload.")

def handle_link(update: Update, context: CallbackContext):
    video_url = update.message.text.strip()
    config = load_config()
    cookies_path = 'cookies.txt'  # adjust path if needed
    simple_logger(f"Received URL: {video_url}")

    update.message.reply_text("Downloading video(s)...")
    try:
        files = download_video(video_url, cookies_path)
        update.message.reply_text("Uploading video(s) to Telegram...")
        for fpath in files:
            with open(fpath, 'rb') as video_file:
                update.message.reply_document(document=video_file)
            os.remove(fpath)
        update.message.reply_text("Done! Video(s) uploaded and removed from server.")
        simple_logger("Download and upload completed successfully.")
    except Exception as e:
        error_msg = f"Error: {e}"
        update.message.reply_text(error_msg)
        simple_logger(error_msg, log_level=logging.ERROR)
