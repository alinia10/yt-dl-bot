import subprocess
import glob
import os
import time
from tqdm import tqdm

def download_video(video_url, cookies_path):
    """
    Downloads videos (single or playlist) using yt-dlp via subprocess with a tqdm progress indicator.
    Returns a list of paths to the downloaded video files.
    """
    command = [
        'yt-dlp',
        video_url,
        '--cookies', cookies_path,
        '--output', './downloads/%(title)s.%(ext)s',
        '--format', 'best',
    ]
    
    # Start the download process.
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Use a tqdm spinner to show progress.
    pbar = tqdm(total=0, bar_format="{desc}", desc="Downloading...", leave=True)
    
    # While the process is running, update progress based on a file-size estimate if available.
    while process.poll() is None:
        # You can add extra logging or file size estimation here if desired.
        time.sleep(0.5)
    
    stdout, stderr = process.communicate()
    pbar.close()
    
    if process.returncode != 0:
        print(f"An error occurred: {stderr}")
        raise subprocess.CalledProcessError(process.returncode, command, output=stdout, stderr=stderr)
    
    # Allow a brief moment for the filesystem to update.
    time.sleep(1)
    
    # Use glob to find all mp4 files in the downloads folder.
    files = glob.glob("./downloads/*.mp4")
    if not files:
        raise Exception("No video file found in downloads folder.")
    
    return files
